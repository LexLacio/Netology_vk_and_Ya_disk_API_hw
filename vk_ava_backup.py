from vk_API import VkUser

with open('vk-token.txt', 'r') as file_object:
    vk_token = file_object.read().strip()
# vk_token = ''    # Впишите токен к vk аккаунту (Альтернативный вариант)
vk_user_id = ''   # Впишите id vk аккаунта
ya_token = ""   # Впишите токен к Yandex диску
ya_folder = 'disk:/vk_avas/'  # Укажите для загрузки существующую папку на ya.disk'е (Например: 'disk:/vk_avas/')

if __name__ == '__main__':
    vk_client = VkUser(vk_token)
    ava_data = vk_client.ava_data_editor(vk_user_id, ya_token, ya_folder)

