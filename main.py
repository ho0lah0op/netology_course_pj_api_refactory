from photo_download import PhotoDownload
from photo_upload import PhotoUpload
from dotenv import dotenv_values

config = dotenv_values(".env")


if __name__ == '__main__':
    user_id = input("Введите ID пользователя VK: ")
    token_yandex = input("Введите токен Яндекс.Диска: ")

    try:
        photo_downloader = PhotoDownload(user_id, config['token_vk'])
        photo_uploader = PhotoUpload(token_yandex)
        folder_name = photo_uploader.create_folder_yadisk('Пользовательские фото VK')
        photo_downloader.download_vk_photo()

        num_photos_to_upload = input("Введите количество фотографий для загрузки на Я.Диск (по умолчанию 5): ")
        if num_photos_to_upload.strip() == "":
            num_photos_to_upload = 5
        else:
            num_photos_to_upload = int(num_photos_to_upload)

        photo_uploader.upload_photo_to_yadisk(folder_name, num_photos=num_photos_to_upload)
    except Exception as e:
        print(f"Ошибка: {str(e)}")
