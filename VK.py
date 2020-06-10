import os
import json

import vk_api
from vk_api.exceptions import BadPassword, ApiError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from YaMusic import YaMusic


class VKAccessException(Exception):
    def __init__(self, text):
        self.txt = text


class VK(object):
    __instance = None
    music_cache_path = "vk_music_from_audio_cache.json"

    def __init__(self):
        self.api = None
        self.__driver = None
        self.password = None
        self.login = None
        self.__ya_music = YaMusic()
        self.__music_from_audios_cache = {}
        self.__load_cache()
        VK.__instance = self

    def __del__(self):
        if self.__driver:
            self.__driver.close()

    def __load_cache(self):
        if os.path.exists(self.music_cache_path):
            with open(self.music_cache_path, "r") as file:
                self.__music_from_audios_cache = json.load(file)

    def __save_cache(self):
        with open(self.music_cache_path, "w") as file:
            json.dump(self.__music_from_audios_cache, file)

    @staticmethod
    def get_instance():
        if VK.__instance:
            return VK.__instance
        else:
            return VK()

    def create_api(self):
        try:
            session = vk_api.VkApi(self.login, self.password)
            session.auth()
            self.api = session.get_api()
            return True
        except BadPassword:
            return False

    def get_text_from_posts(self, id):
        text = ""
        ofs = 0
        while True:
            try:
                posts = self.api.wall.get(owner_id=id, count=100, offset=ofs)
            except ApiError:
                return ""
            for i in posts["items"]:
                text += (self.__get_text_from_post(i))
            ofs += 100
            if ofs >= posts["count"] or ofs >= 1000:
                break

        return text

    def __get_text_from_post(self, post):
        text = ""
        if "copy_history" in post:
            for i in post["copy_history"]:
                text += (self.__get_text_from_post(i))
        if "text" in post:
            text += post["text"] + " "
        return text

    def get_music_from_audios(self, id):
        if str(id) in self.__music_from_audios_cache:
            return self._get_music_from_html(self.__music_from_audios_cache[str(id)])

        if not self.__driver:
            self.__driver = self._create_webdriver()
            self._auth_selenium()
        url = "https://vk.com/audios" + str(id)
        self.__driver.get(url)

        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui_tab_sel"))
        )
        if not str(self.__driver.current_url).endswith(str(id)):
            raise VKAccessException('you do not have access to music')

        text = self.__driver.page_source
        while True:
            for _ in range(20):
                self.__driver.execute_script("window.scrollBy(0,50000);")
            if self.__driver.page_source == text:
                break
            text = self.__driver.page_source

        self.__music_from_audios_cache[str(id)] = text
        self.__save_cache()
        return self._get_music_from_html(text)

    def _auth_selenium(self):
        url = "https://vk.com/"
        self.__driver.get(url)
        field_login = self.__driver.find_element_by_id("index_email")
        field_login.send_keys(self.login)
        field_password = self.__driver.find_element_by_id("index_pass")
        field_password.send_keys(self.password)
        self.__driver.find_element_by_id('index_login_button').click()
        WebDriverWait(self.__driver, 20).until(
            EC.presence_of_element_located((By.ID, "l_pr"))
        )

    def _get_music_from_html(self, text):
        soup = BeautifulSoup(text, "html.parser")
        html_music = soup.findAll('div', class_='audio_row__performer_title')
        music = []

        for html in html_music:
            author = html.find("a").text
            name = html.find("span", class_="audio_row__title_inner _audio_row__title_inner").text
            music.append(self.__ya_music.get_song(name, author))

        self.__ya_music.save_cache()
        return music

    def _create_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(options=chrome_options)




