import requests
import os
import time
import json
import sys
from tqdm import tqdm


class PhotoUpload:

    def __init__(self, token_yandex: str):
        self.token_yandex = token_yandex
        self.direct = r'C:\Personal\Netology\Misc\vk_photo'

    def check_status_code(self, response):
        response.raise_for_status()  # Этот метод вызовет исключение, если ответ содержит код ошибки

    def upload_photo_to_yadisk(self, path, num_photos=5):
        try:
            os.chdir(self.direct)
            files_list = [name for name in os.listdir(self.direct) if name.endswith(".jpg")]
            sorted_photos = sorted(files_list, key=lambda x: os.path.getsize(x), reverse=True)
            pbar = tqdm(total=min(num_photos, len(sorted_photos)), desc='Отправление фотографий на Я.диск')
            number_of_sent = 0
            for name_file in sorted_photos[:num_photos]:
                number_of_sent += 1
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'OAuth {self.token_yandex}'
                }
                params = {
                    'path': f'{path}/{name_file}',
                    'overwrite': True
                }
                upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
                response = requests.get(upload_url, headers=headers, params=params)
                self.check_status_code(response)  # Проверка статус-кода ответа
                href = response.json().get("href", "")
                response = requests.api.put(href, data=open(name_file, 'rb'), headers=headers)
                self.check_status_code(response)  # Проверка статус-кода ответа
                pbar.update(1)
                time.sleep(0.5)
            pbar.close()
            if number_of_sent == 1:
                print(f'\nНа Я.диск отправлена {number_of_sent} фотография!')
            else:
                print(f'\nНа Я.диск отправлено {number_of_sent} фотографий!')
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            sys.exit(1)

    def create_folder_yadisk(self, name_folder: str):
        try:
            headers = {
                "Accept": 'application/json',
                'Authorization': f'OAuth {self.token_yandex}'
            }
            params = {
                'path': f'/{name_folder}',
            }
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
            response = requests.put(upload_url, headers=headers, params=params)
            if response.status_code == 409:
                print(f"Папка с именем '{name_folder}' уже существует на Яндекс.Диске.")
                return name_folder
            self.check_status_code(response)  # Проверка статус-кода ответа
            return name_folder
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            sys.exit(1)