import os
import requests
import time
from dotenv import load_dotenv
from urllib.parse import urljoin
from download_comics import download_random_comic


API_VERSION = 5.131


def get_upload_url(access_token, group_id, api_version=API_VERSION):
    base_vk_url = 'https://api.vk.com/method/'
    path = 'photos.getWallUploadServer'
    params = {'access_token': access_token,
              'group_id': group_id,
              'v': api_version}
    response = requests.get(urljoin(base_vk_url, path), params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_img(upload_url, image_path):
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
    response = requests.post(upload_url, files=files)
    response.raise_for_status()
    json_object = response.json()
    return json_object['server'], json_object['photo'], json_object['hash']


def save_photo(access_token,
               group_id,
               server,
               photo,
               hash,
               api_version=API_VERSION):
    base_vk_url = 'https://api.vk.com/method/'
    path = 'photos.saveWallPhoto'
    params = {'access_token': access_token,
              'server': server,
              'photo': photo,
              'hash': hash,
              'group_id': group_id,
              'v': api_version}
    response = requests.get(urljoin(base_vk_url, path), params)
    response.raise_for_status()
    photo = response.json()['response'][0]
    return photo['id'], photo['owner_id']


def publish_photo(access_token,
                  owner_id,
                  message,
                  attachments,
                  from_group=1,
                  api_version=API_VERSION):
    base_vk_url = 'https://api.vk.com/method/'
    path = 'wall.post'
    params = {'access_token': access_token,
              'owner_id': owner_id,
              'message': message,
              'from_group': from_group,
              'attachments': attachments,
              'v': api_version}
    response = requests.get(urljoin(base_vk_url, path), params)
    response.raise_for_status()


if __name__ == '__main__':
    load_dotenv()
    GROUP_ID = os.environ['VK_GROUP_ID']
    ACCESS_TOKEN = os.environ['VK_ACCESS_TOKEN']

    while True:
        try:
            image_path, comment = download_random_comic()
            upload_url = get_upload_url(ACCESS_TOKEN, GROUP_ID)
            server, photo, hash = upload_img(upload_url, image_path)
            photo_id, owner_id = save_photo(ACCESS_TOKEN, GROUP_ID, 
                                            server, photo, hash)
            attachment = 'photo' + str(owner_id) + '_' + str(photo_id)
            publish_photo(ACCESS_TOKEN, "-" + GROUP_ID, comment, attachment)
            os.remove(image_path)
            break
        except requests.ConnectionError:
            print('Connection error. Retrying in 5 seconds')
            time.sleep(5)
            continue
