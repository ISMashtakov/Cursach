
import vk_api
from vk_api.exceptions import BadPassword
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class VKAccessException(Exception):
    def __init__(self, text):
        self.txt = text


class VKAccessMusicError(VKAccessException):
    def __init__(self, text):
        self.txt = text


class VK:
    def __init__(self):
        self._api = None
        self.driver = self._create_webdriver()
        self.password = None
        self.login = None

    def get_api(self):
        return self._api

    def create_api(self):
        try:
            self._session = vk_api.VkApi(self.login, self.password)
            self._session.auth()
            self._api = self._session.get_api()
            return True
        except BadPassword:
            return False

    def auth_selenium(self):
        url = "https://vk.com/"
        self.driver.get(url)
        field_login = self.driver.find_element_by_id("index_email")
        field_login.send_keys(self.login)
        field_password = self.driver.find_element_by_id("index_pass")
        field_password.send_keys(self.password)
        self.driver.find_element_by_id('index_login_button').click()
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "l_pr"))
        )

    def is_connected(self):
        return self._user_session is not None

    def get_all_friends(self):
        friends = self._api.friends.get(fields="nickname,photo_50")
        return friends

    def get_info(self, user, field):
        return self._api.users.get(user_ids=user, fields=field)[0]

    def get_list_of_music_from_walls_in_page(self, to_id):
        all_music = []
        ofs = 0
        while True:
            posts = self._api.wall.get(owner_id=to_id, count=100, offset=ofs)
            for i in posts["items"]:
                all_music.extend(self._find_music_in_post(i))
            ofs += 100
            if ofs >= posts["count"]:
                break
        return all_music

    def get_user_groups(self, user):
        vk_groups = self._api.groups.get(user_id=user)
        return self._get_groups_from_groups_ids(vk_groups["items"])

    def get_general_groups(self, to_id1, to_id2):
        groups1 = set(self._api.groups.get(user_id=to_id1)['items'])
        groups2 = set(self._api.groups.get(user_id=to_id2)['items'])
        general = groups1.intersection(groups2)
        return self._get_groups_from_groups_ids(list(general))

    def get_post_with_like(self, user):
        likes = []
        groups = self.get_user_groups(user)
        groups = groups[:5 if len(groups) >= 5 else len(groups)]
        for group in groups:
            ofs = 0
            print(group["name"])
            while True:
                posts = self._api.wall.get(owner_id=-group["id"], count=10, offset=ofs)
                for i in posts["items"]:
                    if self._api.likes.isLiked(user_id=user, type='post', item_id=i['id'])['liked'] == 1:
                        likes.append(i)
                        print(i)
                ofs += 10
                print(ofs)
                if ofs >= posts["count"] or ofs >= 100:
                    break
        return likes

    def get_all_music(self, user):
        url = "https://vk.com/audios" + str(user)
        self.driver.get(url)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui_tab_sel"))
        )
        if not str(self.driver.current_url).endswith(str(user)):
            raise VKAccessMusicError('you do not have access to music')

        text = self.driver.page_source
        while True:
            for _ in range(20):
                self.driver.execute_script("window.scrollBy(0,50000);")
            if self.driver.page_source == text:
                break
            text = self.driver.page_source

        return self._get_music_from_html(text)

    def _get_music_from_html(self, text):
        soup = BeautifulSoup(text, "html.parser")
        html_music = soup.findAll('div', class_='audio_row__performer_title')
        music = []
        for html in html_music:
            author = html.find("a").text
            name = html.find("span", class_="audio_row__title_inner _audio_row__title_inner").text
            music.append({"name": name, "author": author})
        return music

    def _create_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options)

    def _find_music_in_post(self, post):
        list_for_music = []
        if "copy_history" in post:
            for i in post["copy_history"]:
                list_for_music.extend(self._find_music_in_post(i))
        if "attachments" in post:
            for i in post["attachments"]:
                if "type" in i and i["type"] == "audio":
                    # Нашёл аудиозапись на стене
                    list_for_music.append({"author": i["audio"]["artist"], "name": i["audio"]["title"]})
        return list_for_music

    def _get_groups_from_groups_ids(self, groups_ids):
        if not groups_ids:
            return []
        vk_groups_info = self._api.groups.getById(group_ids=groups_ids)
        groups = []
        for i in vk_groups_info:
            groups.append({"id": i["id"], "name": i["name"]})
        return groups

me = None
milena = 191776959
udin = 420205723
vk = VK()
vk.login = "89063577290"
vk.password = "Gariktron1"
vk.create_api()
print(vk.getLikes(me))
pass
