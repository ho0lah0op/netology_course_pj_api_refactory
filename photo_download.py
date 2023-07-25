import requests
import os
import time
import json
import sys
from tqdm import tqdm
from pprint import pprint


class PhotoDownload:

    def __init__(self, user_id: str, token_vk: str):
        self.user_id = user_id
        self.token_vk = token_vk
        self.direct = r'C:\Personal\Netology\Misc\vk_photo'

    def check_status_code(self, response):
        response.raise_for_status()  # Этот метод вызовет исключение, если ответ содержит код ошибки

    def download_vk_photo(self):
        try:
            os.chdir(self.direct)
            url_vk = 'https://api.vk.com/method/photos.get'
            params_vk = {
                'owner_id': self.user_id,
                'album_id': 'profile',
                'extended': '1',
                'access_token': self.token_vk,
                'v': '5.131'
            }
            res = requests.get(url_vk, params=params_vk)
            self.check_status_code(res)  # Проверка статус-кода ответа
            response_json = res.json()
            pprint(response_json)
            photo_items = response_json['response']['items']
            with tqdm(total=len(photo_items), desc='Загрузка фотографий') as pbar:
                logs_list = []
                for item in photo_items:
                    url_photo = item['sizes'][-1]['url']
                    self.size = item['sizes'][-1]['type']
                    response = requests.get(url_photo)
                    self.check_status_code(response)  # Проверка статус-кода ответа
                    filename = f"{item['likes']['count']}.jpg"
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    pbar.update(1)
                    time.sleep(1)
                    download_log = {'file_name': filename, 'size': self.size}
                    logs_list.append(download_log)

            # Сохранение JSON после завершения цикла
            save_json_data(logs_list, f'{self.direct}/log.json')

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            sys.exit(1)


def save_json_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)