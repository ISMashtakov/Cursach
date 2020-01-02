import vk_api

import WorkWithVK as myVk

vk_session = vk_api.VkApi('89063577290', 'Gariktron1')
vk_session.auth()

vk = vk_session.get_api()
myVk.get_list_of_music_from_walls_in_page(vk, 220697751)
