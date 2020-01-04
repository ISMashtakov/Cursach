import vk_api

from myGUI import MyWindow

vk_session = vk_api.VkApi('89063577290', 'Gariktron1')
vk_session.auth()

vk = vk_session.get_api()
# myVk.get_post_with_like(vk, 235832830)
# myVk.get_music()
# myVk.get_general_groups(vk, 191776959, 220697751)

window = MyWindow()

