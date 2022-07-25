import configparser

from vk_API import VkUser
from vk_API import YandexDisk

config = configparser.ConfigParser()
config.read("settings.ini")

vk_token = config["VK"]["token"]
vk_user_id = config["VK"]["user_id"]
vk_user_screen_name = config["VK"]["user_screen_name"]
vk_avas_count = config["VK"]["avas_count"]
ya_token = config["Yandex_disk"]["token"]
ya_folder = config["Yandex_disk"]["ya_folder"]

if __name__ == '__main__':
    ya_client = YandexDisk(ya_token)
    new_folder = ya_client.folder_creation(ya_folder)
    vk_client = VkUser(vk_token)
    if not vk_user_id:
        vk_user_id = vk_client.get_user_id(vk_user_screen_name)
        ava_data = vk_client.ava_data_editor(vk_user_id, vk_avas_count, ya_token, ya_folder)
    else:
        ava_data = vk_client.ava_data_editor(vk_user_id, vk_avas_count, ya_token, ya_folder)

