from VK import VK
from VK import VKAccessException


class User:
    __all_user = {}

    def __init__(self, id, first_name=None, last_name=None, image=None, music_from_page=None, music_from_audios=None, friends=None, groups=None, inf=None):
        self.id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__image = image
        self.__music_from_page = music_from_page
        self.__music_from_audios = music_from_audios
        self.__friends = friends
        self.__groups = groups
        self.__vk = VK.get_instance()
        self.__inf = inf
        User.__all_user[id] = self

    @property
    def groups(self):
        if self.__groups is None:
            self.__groups = [i["name"] for i in self.__vk.api.groups.get(user_id=self.id, extended=1)["items"]]
        return self.__groups

    @property
    def friends(self):
        if self.__friends is None:
            self.__friends = []
            friends = self.__vk.api.friends.get(user_id=self.id, order='hints', fields="nickname")
            for friend in friends['items']:
                if friend['id'] in User.__all_user:
                    self.__friends.append(User.__all_user[friend['id']])
                else:
                    self.__friends.append(User(id=friend['id'],
                                               first_name=friend["first_name"], last_name=friend["last_name"]))
        return self.__friends

    @property
    def image(self):
        if self.__image is None:
            self.__image = self.__vk.api.users.get(user_id=self.id, fields="photo_50")
        return self.__image

    @property
    def music_from_audios(self):
        if self.__music_from_audios is None:
            try:
                self.__music_from_audios = self.__vk.get_music_from_audios(self.id)
            except VKAccessException:
                self.__music_from_audios = []
        return self.__music_from_audios

    @property
    def music_from_page(self):
        if self.__music_from_page is None:
            try:
                self.__music_from_page = self.__vk.get_music_from_page(self.id)
            except VKAccessException:
                self.__music_from_page = []
        return self.__music_from_page

    @property
    def first_name(self):
        if self.__first_name is None:
            self.__updates_names()
        return self.__first_name

    @property
    def last_name(self):
        if self.__last_name is None:
            self.__updates_names()
        return self.__last_name

    def __updates_names(self):
        self.__first_name = {}
        self.__last_name = {}
        res = self.__vk.api.users.get(user_id=self.id, fields="first_name", name_case='nom')
        self.__first_name["I"] = res[0]["first_name"]
        self.__last_name["I"] = res[0]["last_name"]
        res = self.__vk.api.users.get(user_id=self.id, fields="first_name", name_case='gen')
        self.__first_name["R"] = res[0]["first_name"]
        self.__last_name["R"] = res[0]["last_name"]
        res = self.__vk.api.users.get(user_id=self.id, fields="first_name", name_case='dat')
        self.__first_name["D"] = res[0]["first_name"]
        self.__last_name["D"] = res[0]["last_name"]
        res = self.__vk.api.users.get(user_id=self.id, fields="first_name", name_case='acc')
        self.__first_name["V"] = res[0]["first_name"]
        self.__last_name["V"] = res[0]["last_name"]
        res = self.__vk.api.users.get(user_id=self.id, fields="first_name", name_case='ins')
        self.__first_name["T"] = res[0]["first_name"]
        self.__last_name["T"] = res[0]["last_name"]
        res = self.__vk.api.users.get(user_id=self.id, fields="first_name", name_case='abl')
        self.__first_name["P"] = res[0]["first_name"]
        self.__last_name["P"] = res[0]["last_name"]

    @property
    def inf(self):
        if not self.__inf:
            self.__inf = {}
            res = self.__vk.api.users.get(user_id=self.id, fields="bdate,home_town,education", name_case='abl')
            self.__inf["bdate"] = res[0].get("bdate", None)
            self.__inf["home_town"] = res[0].get("home_town", None)
            self.__inf["education"] = res[0].get("university_name", None)
        return self.__inf

