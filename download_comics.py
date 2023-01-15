import urllib
import os
from support_funcs import get_response
from random import randint


CURRENT_COMICS_URL = 'https://xkcd.com/info.0.json'


def download_photo(url, folderpath):
    os.makedirs(folderpath, exist_ok=True)
    response = get_response(url)
    filepath = os.path.join(folderpath, get_filename(url))
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def get_filename(url):
    path = urllib.parse.urlsplit(url).path
    filepath, filename = os.path.split(path)
    return filename


def download_comics(url, folderpath='img'):
    response = get_response(url)
    comics = response.json()
    file = download_photo(comics['img'], folderpath)
    return file, comics['alt']


def get_current_num(current_url):
    response = get_response(current_url)
    return response.json()['num']


def download_random_comics(current_url=CURRENT_COMICS_URL, folderpath='img'):
    random_num = randint(1, get_current_num(current_url))
    random_comics_url = f'https://xkcd.com/{random_num}/info.0.json'
    file, comment = download_comics(random_comics_url, folderpath)
    return file, comment


if __name__ == '__main__':
    COMICS_URL = 'https://xkcd.com/614/info.0.json'
    print(download_comics(COMICS_URL))

