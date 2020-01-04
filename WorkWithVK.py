import requests
import urllib
import lxml.html

import vk_api


def create_vk(login, password):
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()

    vk = vk_session.get_api()
    return vk

def create_session(login, password):
    url = 'https://vk.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive', 'DNT': '1'}
    session = requests.Session()
    data = session.get(url, headers=headers)
    page = lxml.html.fromstring(data.content)

    form = page.forms[0]
    form.fields['email'] = login
    form.fields['pass'] = password

    response = session.post(form.action, data=form.form_values())
    if 'onLoginDone' in response.text:
        return session
    session.close()
    return False


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
        for i in posts["items"]:
            find_music_in_post(all_music, i)
        ofs += 100
        if ofs >= posts["count"]:
            break
    print(all_music)


def get_general_groups(vk, to_id1, to_id2):
    groups1 = set(vk.groups.get(user_id=to_id1)['items'])
    groups2 = set(vk.groups.get(user_id=to_id2)['items'])
    general = groups1.intersection(groups2)
    return general


def get_post_with_like(vk, to_id):
    all_likes = []
    public = vk.groups.get(user_id=to_id)
    print(public['count'])
    for Id in public['items']:
        print(Id)
        ofs = 0
        while True:
            posts = vk.wall.get(owner_id=-Id, count=10, offset=ofs)
            for i in posts["items"]:
                if vk.likes.isLiked(user_id=to_id, type='post', item_id=i['id'])['liked'] == 1:
                    print(i)
                    all_likes.append(i)
            ofs += 100
            if ofs >= posts["count"] or ofs > 0:
                break
    print(all_likes)

# print(bytes(response.content).decode('utf-8'))
