import datetime
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from additional_functions import download_image, get_file_extension


def fetch_astronomy_picture_from_nasa(count: int, nasa_request_params: dict):
    apod_images_dir = 'images/apod_images/'
    Path(apod_images_dir).mkdir(parents=True, exist_ok=True)
    url = 'https://api.nasa.gov/planetary/apod'
    nasa_request_params['count'] = count
    response = requests.get(url, params=nasa_request_params)
    response.raise_for_status()
    links_img = [link['hdurl'] for link in response.json()]
    for number_img, link_img in enumerate(links_img, start=1):
        img_extension = get_file_extension(link_img)
        path_img = f'{apod_images_dir}apod{str(number_img)}{img_extension}'
        download_image(link_img, path_img)


def fetch_EPIC_photo(count: int, nasa_request_params: dict):
    epic_images_dir = 'images/EPIC_images/'
    Path(epic_images_dir).mkdir(parents=True, exist_ok=True)
    json_url = 'https://epic.gsfc.nasa.gov/api/natural'
    photo_url = 'https://api.nasa.gov/EPIC/archive/natural/'
    response = requests.get(json_url)
    response.raise_for_status()
    images = response.json()
    for index in range(count):
        date = datetime.datetime.fromisoformat(images[index]['date'])
        date = date.strftime("%Y/%m/%d")
        img_id = images[index]['image']
        link_img = f'{photo_url}/{date}/png/{img_id}.png'
        path_img = f'{epic_images_dir}{img_id}.png'
        download_image(link_img, path_img, params=nasa_request_params)


def main():
    nasa_api_token = os.getenv('NASA_API_TOKEN')
    nasa_request_params = {'api_key': nasa_api_token}
    apod_count = int(input('Введите сколько фото дня от NASA вы хотите скачать: '))
    epic_count = int(input('Введите сколько фото Земли вы хотите скачать: '))
    fetch_astronomy_picture_from_nasa(apod_count, nasa_request_params)
    fetch_EPIC_photo(epic_count, nasa_request_params)


if __name__ == '__main__':
    main()
