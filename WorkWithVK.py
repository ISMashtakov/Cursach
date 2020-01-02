import requests
import urllib.request

import vk_api


def find_music_in_post(list_for_music, post):
    if "copy_history" in post:
        for i in post["copy_history"]:
            find_music_in_post(list_for_music, i)
    if "attachments" in post:
        for i in post["attachments"]:
            if "type" in i and i["type"] == "audio":
                # Нашёл аудиозапись на стене
                list_for_music.append([i["audio"]["artist"], i["audio"]["title"]])


def get_list_of_music_from_walls_in_page(vk, to_id):
    all_music = []
    ofs = 0
    while True:
        posts = vk.wall.get(owner_id=to_id, count=100, offset=ofs)
        k = 1
        for i in posts["items"]:
            k += 1
            find_music_in_post(all_music, i)
        ofs += 100
        if ofs >= posts["count"]:
            break
    print(all_music)


def get_list_of_music(vk, to_id):
    token = requests.get('http://api.vk.com/oauth/authorize?'
                         'client_id=7227453'
                         '&redirect_uri=http://api.vk.com/blank.html'
                         '&scope=audio'
                         '&display=page'
                         '&response_type=token')
    print(token.status_code)