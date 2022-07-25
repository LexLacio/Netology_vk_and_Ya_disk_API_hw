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

    def folder_creation(self, folder_name):

        """Функция создаёт папки на ya.disk"""

        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = self.get_headers()
        params = {"path": folder_name}
        response = requests.put(upload_url, headers=headers, params=params)
        if response.status_code == 201:
            print(f'Папка {folder_name} cоздана на Яндекс диске')
        else:
            print(f'Папка {folder_name} уже есть на Яндекс диске')
            # print(response.status_code)

    def ava_uploader(self, ava_url, ava_name, ya_folder):

        """Функция загружает аватарки по ссылке на ya.disk"""

        link = ava_url
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        file_path = 'disk:/' + ya_folder + '/' + str(ava_name)
        headers = self.get_headers()
        params = {"url": link, "path": file_path}
        response = requests.post(upload_url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 202:
            print(f'Аватарка {ava_name} загружена на Яндекс диск')
        else:
            print(response.status_code)

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        # pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, list_name, disk_file_path):
        with open('ava_list.json', "w") as file:
            json.dump(list_name, file, ensure_ascii=False, indent=2)
        href = self._get_upload_link(disk_file_path='disk:/' + disk_file_path + '/ava_list.json').get("href", "")
        response = requests.put(href, data=open('ava_list.json', 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('ava_list.json файл-легенда аватарок загружен на Яндекс диск')


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.params = {
            'access_token': token,
            'v': '5.131'
        }

    def get_user_id(self, screen_name):

        """Функция получает user_id по screen_name"""

        URL = 'https://api.vk.com/method/users.get'
        user_screen_name = {'user_ids': screen_name}
        res = requests.get(URL, params={**self.params, **user_screen_name})
        vk_user_id = res.json()['response'][0]['id']
        # print(f'screen_name {screen_name} соответствует user_id {vk_user_id }')
        return vk_user_id

    def ava_download(self, User_id, avas_count):

        """Функция скачивает аватарки по UserId и выводит результат в json"""

        ava_download_url = self.url + 'photos.get'
        ava_download_params = {
            'owner_id': User_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1,
            'count': avas_count
        }
        ava_download_result = requests.get(ava_download_url, params={**self.params, **ava_download_params}).json()
        return ava_download_result

    def ava_data_editor(self, User_id, avas_count, ya_token, ya_folder):

        """Функция обрабатывает json аватарок и загружает поштучно на yandex диск.
        Выводит пронумерованный словарь с значениями:
        имя файла: количество лайков + дата,
        размер файла: формат файла"""

        ya = YandexDisk(token=ya_token)
        ava_download_res = self.ava_download(User_id, avas_count)
        ava_data = ava_download_res['response']['items']
        ava_list = {}  # Создание словаря для json файла с легендой
        ava_list_uniq = []  # Список для проверки уникальности имён аватарок
        counter = 0
        for ava in ava_data:
            counter += 1
            url_list = []
            url_type_list = []
            for url in ava['sizes']:  # Цикл перебирает ссылки и типы и выводит самые последние ссылки с типами
                url_list.append(url['url'])
                url_type_list.append(url['type'])
            ava_link = url_list[-1]  # Получаем последнюю из списка ссылку на аву
            ava_size = url_type_list[-1]  # Получаем тип/размер авы для последней из списка
            ava_date = str(time.strftime('%Y-%m-%d', time.localtime(int(ava["date"]))))
            ava_name = str(ava["likes"]['count']) + '.jpeg'
            if ava_name in ava_list_uniq:  # Проверка уникальности имён аватарок
                ava_name = str(ava["likes"]['count']) + '_' + ava_date + '.jpeg'
            else:
                pass
            ya.ava_uploader(ava_link, ava_name, ya_folder)
            ava_list_uniq.append(ava_name)

            ava_list[counter] = [
                {"file_name": ava_name, "size": ava_size}]  # Добавление значений в словарь для json файла с легендой
        ya.upload_file_to_disk(ava_list, ya_folder)  # Вызов функции загрузки json файла с легендой
        # pprint(ava_list)
        # print(ava_list_uniq)
        return ava_list
