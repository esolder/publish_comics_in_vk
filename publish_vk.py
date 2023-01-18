import os
import requests
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
    upload = response.json()
    return upload['server'], upload['photo'], upload['hash']


def save_photo(access_token,
               group_id,
               server,
               photo,
               hash_sum,
               api_version=API_VERSION):
    base_vk_url = 'https://api.vk.com/method/'
    path = 'photos.saveWallPhoto'
    params = {'access_token': access_token,
              'server': server,
              'photo': photo,
              'hash': hash_sum,
              'group_id': group_id,
              'v': api_version}
    response = requests.get(urljoin(base_vk_url, path), params)
    response.raise_for_status()
    photo = response.json()['response'][0]
    return photo['id'], photo['owner_id']


def publish_photo(access_token,
                  group_id,
                  message,
                  photo_owner_id,
                  photo_id,
                  from_group=1,
                  api_version=API_VERSION):
    base_vk_url = 'https://api.vk.com/method/'
    path = 'wall.post'
    attachment = f'photo{photo_owner_id}_{photo_id}'
    owner_id = f'-{group_id}'
    params = {'access_token': access_token,
              'owner_id': owner_id,
              'message': message,
              'from_group': from_group,
              'attachments': attachment,
              'v': api_version}
    response = requests.get(urljoin(base_vk_url, path), params)
    response.raise_for_status()


if __name__ == '__main__':
    load_dotenv()
    group_id = os.environ['VK_GROUP_ID']
    access_token = os.environ['VK_ACCESS_TOKEN']

    folderpath = 'img'
    os.makedirs(folderpath, exist_ok=True)

    try:
        image_path, comment = download_random_comic(folderpath=folderpath)
        upload_url = get_upload_url(access_token, group_id)
        server, photo, hash_sum = upload_img(upload_url, image_path)
        photo_id, photo_owner_id = save_photo(access_token, group_id,
                                              server, photo, hash_sum)
        publish_photo(access_token, group_id, comment,
                      photo_owner_id, photo_id)
    finally:
        os.remove(image_path)
