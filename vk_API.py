import requests

import time

import json


from pprint import pprint


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def ava_uploader(self, ava_url, ava_name, ya_folder):

        """Функция загружает аватарки по ссылке на ya.disk"""

        link = ava_url
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        file_path = ya_folder + str(ava_name)
        headers = self.get_headers()
        params = {"url": link, "path": file_path}
        response = requests.post(upload_url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 202:
            print("Success")
        else:
            print(response.status_code)

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path):
        href = self._get_upload_link(disk_file_path=disk_file_path + 'ava_list.json').get("href", "")
        response = requests.put(href, data=open('ava_list.json', 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.params = {
            'access_token': token,
            'v': '5.131'
        }

    def ava_download(self, User_id):

        """Функция скачивает аватарки по UserId и выводит результат в json"""

        ava_download_url = self.url + 'photos.get'
        ava_download_params = {
            'owner_id': User_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1
        }
        ava_download_result = requests.get(ava_download_url, params={**self.params, **ava_download_params}).json()
        return ava_download_result

    def ava_data_editor(self, User_id, ya_token, ya_folder):

        """Функция обрабатывает json аватарок и загружает поштучно на yandex диск.
        Выводит пронумерованный словарь с значениями:
        имя файла: количество лайков + дата,
        размер файла: формат файла"""

        ya = YandexDisk(token=ya_token)
        ava_download_res = self.ava_download(User_id)
        ava_data = ava_download_res['response']['items']
        ava_list = {}
        counter = 0
        for ava in ava_data:
            counter += 1
            url_list = []
            url_type_list = []
            for url in ava['sizes']:  # Цикл перебирает ссылки и типы и выводит самые последние ссылки с типами
                url_list.append(url['url'])
                url_type_list.append(url['type'])
            ava_link = url_list[-1]   # Получаем последнюю из списка ссылку на аву
            ava_size = url_type_list[-1]   # Получаем тип/размер авы для последней из списка
            ava_date = str(time.strftime('%Y-%m-%d', time.localtime(int(ava["date"]))))
            ava_name = str(ava["likes"]['count']) + '_' + ava_date + '.jpeg'
            ya.ava_uploader(ava_link, ava_name, ya_folder)
            ava_list[counter] = [{"file_name": ava_name, "size": ava_size}] # Создание json файла с легендой
        with open('ava_list.json', "w") as file:
            json.dump(ava_list, file, ensure_ascii=False, indent=2)
        ya.upload_file_to_disk(ya_folder)  # Загрузка json файла с легендой
        pprint(ava_list)
        return ava_list


