import random
import string
import time
from collections import Counter
import threading

from pymorphy2 import MorphAnalyzer

from user import User
from YaMusic import all_genres
from VK import VK


class Description:
    month = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
    description_good_genres = [
        "Они оба фанаты {I}. Или {I} сейчас в моде, или они оба странные.",
        "Есть сотни жанров, но они оба слушают {I}."
    ]
    description_bad_genres = [
        "Из всего множества жанров {FNI1} выбрал {V1}, а {FNI2} - {V2}."
    ]
    description_general_authors = [
        "{FNI1} и {FNI2} оба слушают {au}.",
        "наверно только {FNI1} и {FNI2} слушают {au}."
    ]
    description_general_titles = [
        "{t} не лучшая из песен этого автора, но {FND1} и {FND2} нравится."
    ]
    description_not_general_authors = [
        "{FND1} и {FND2} нравятся разные исполнители."
    ]
    description_not_general_titles = [
        "{FNI1} и {FNI2} не смогут обсудить какие-то песни, так как слушают разные."
    ]
    description_close_inf = [
        "{FND} жалко личной информации для вас."
    ]
    description_close_inf_both = [
        "Им жалко личной информации для вас."
    ]
    description_general_year = [
        "{y} - хороший год, так как {FNI1} и {FNI2} родились тогда."
    ]
    description_general_month = [
        "{m} - хороший месяц, так как у {FNR1} и {FNR2} день рождения."
    ]
    description_general_day = [
        "{d}, наверное, любимое число {FNR1} и {FNR2}, так как они родились в такое число."
    ]
    description_general_home_town = [
        "{h} - лучший город на земле по мнению {FNR1} и {FNR2}, так как это их родина."
    ]
    description_general_university = [
        "{u} всё же смог заманить {FNR1} и {FNR2} к себе."
    ]
    description_general_words = [
        "{FND1} и {FND2} нравится слово '{w}'. Иначе как объяснить: почему оно так часто встречаеться в их постах."
    ]
    description_not_general_words = [
        "посты {FNR1} и {FNR2} сложно перепутать, так как они совершенно разные."
    ]
    description_general_groups = [
        "посты в '{g}', видать, очень нравятся {FND1} и {FND2} ."
    ]
    description_not_general_groups = [
        "глядя на паблики {FNR1} и {FNR2}, увлечения у них сильно отличаются."
    ]

    def __init__(self, user1: User, user2: User):
        self.user1 = user1
        self.user2 = user2
        self.kwargs = {"FNI1": user1.first_name["I"], "FNI2": user2.first_name["I"], "LNI1": user1.last_name["I"], "LNI2": user2.last_name["I"],
                       "FNR1": user1.first_name["R"], "FNR2": user2.first_name["R"], "LNR1": user1.last_name["R"], "LNR2": user2.last_name["R"],
                       "FND1": user1.first_name["D"], "FND2": user2.first_name["D"], "LND1": user1.last_name["D"], "LND2": user2.last_name["D"],}
                       # "FNV1": user1.first_name["V"], "FNV2": user2.first_name["V"], "LNV1": user1.last_name["V"], "LNV2": user2.last_name["V"],
                       # "FNT1": user1.first_name["T"], "FNT2": user2.first_name["T"], "LNT1": user1.last_name["T"], "LNT2": user2.last_name["T"],
                       # "FNP1": user1.first_name["P"], "FNP2": user2.first_name["P"], "LNP1": user1.last_name["P"], "LNP2": user2.last_name["P"]}
        self.kwargs1 = {"FNI": user1.first_name["I"], "LNI": user1.last_name["I"],
                        "FNR": user1.first_name["R"], "LNR": user1.last_name["R"],
                        "FND": user1.first_name["D"], "LND": user1.last_name["D"],}
                        # "FNV": user1.first_name["V"], "LNV": user1.last_name["V"],
                        # "FNT": user1.first_name["T"], "LNT": user1.last_name["T"],
                        # "FNP": user1.first_name["P"], "LNP": user1.last_name["P"],}

        self.kwargs2 = {"FNI": user2.first_name["I"], "LNI": user2.last_name["I"],
                        "FNR": user2.first_name["R"], "LNR": user2.last_name["R"],
                        "FND": user2.first_name["D"], "LND": user2.last_name["D"],}
                        # "FNV": user2.first_name["V"], "LNV": user2.last_name["V"],
                        # "FNT": user2.first_name["T"], "LNT": user2.last_name["T"],
                        # "FNP": user2.first_name["P"], "LNP": user2.last_name["P"],}

    def get_good_genres(self, genre):
        return random.choice(self.description_good_genres).format(I=all_genres[genre]["I"],
                                                                  R=all_genres[genre]["R"],
                                                                  **self.kwargs)

    def get_bad_genres(self, genre1, genre2):
        return random.choice(self.description_bad_genres).format(I1=all_genres[genre1]["I"],
                                                                 R1=all_genres[genre1]["R"],
                                                                 I2=all_genres[genre2]["I"],
                                                                 R2=all_genres[genre2]["R"],
                                                                 V1=all_genres[genre1]["V"],
                                                                 V2=all_genres[genre2]["V"],
                                                                 **self.kwargs)

    def get_general_authors(self, authors):
        if authors:
            return random.choice(self.description_general_authors).format(au=random.choice(list(authors)), **self.kwargs)
        else:
            return random.choice(self.description_not_general_authors).format(**self.kwargs)

    def get_general_titles(self, titles):
        if titles:
            return random.choice(self.description_general_titles).format(t=random.choice(list(titles)), **self.kwargs)
        else:
            return random.choice(self.description_not_general_titles).format(**self.kwargs)

    def get_without_inf(self, user=None):
        if user:
            return random.choice(self.description_close_inf).format(**(self.kwargs1 if user is self.user1 else self.kwargs2))
        else:
            return random.choice(self.description_close_inf_both)

    def get_general_year(self, year):
        return random.choice(self.description_general_year).format(y=year, **self.kwargs)

    def get_general_month(self, month):
        return random.choice(self.description_general_month).format(m=self.month[int(month)-1], **self.kwargs)

    def get_general_day(self, day):
        return random.choice(self.description_general_day).format(d=day, **self.kwargs)

    def get_general_home_town(self, ht):
        return random.choice(self.description_general_home_town).format(h=ht, **self.kwargs)

    def get_general_university(self, uni):
        return random.choice(self.description_general_university).format(u=uni, **self.kwargs)

    def get_general_word(self, words):
        return random.choice(self.description_general_words).format(w=random.choice(list(words)), **self.kwargs)

    def get_not_general_word(self):
        return random.choice(self.description_not_general_words).format(**self.kwargs)

    def get_general_groups(self, groups):
        return random.choice(self.description_general_groups).format(g=random.choice(list(groups)), **self.kwargs)

    def get_not_general_groups(self):
        return random.choice(self.description_not_general_groups).format(**self.kwargs)


class UsersComparator:
    def __init__(self, user1: User, user2: User, bar=None):
        self.user1 = user1
        self.user2 = user2
        self.vk = VK.get_instance()
        self.descriptions = Description(user1, user2)
        self.user1_all_music = None
        self.user2_all_music = None
        self.bar = bar
        self.progress = 0
        self.need_update = True

    def _update_bar(self):
        while self.need_update:
            time.sleep(0.1)
            self.bar["value"] = self.progress + self.vk.progress*35

    def compare_music(self):
        self.user1_all_music = self.user1.music_from_audios
        self.progress = 35
        self.vk.progress = 0
        self.user2_all_music = self.user2.music_from_audios
        self.progress = 70
        self.vk.progress = 0
        if self.user1_all_music == self.user2_all_music:
            return 50, ''
        if not self.user1_all_music or not self.user2_all_music:
            return 0, ''
        general_title = set()
        general_author = set()
        for mus1 in self.user1_all_music:
            for mus2 in self.user2_all_music:
                if mus1.name == mus2.name and mus1.author == mus2.author:
                    title = "{} - {}".format(mus1.author, mus1.name)
                    general_title.add(title)

                a = set(mus1.author).intersection(set(mus2.author))
                if a:
                    general_author = general_author.union(a)
        com_gen = self.compare_genres()
        score = com_gen[0]
        description = com_gen[1] + "\n"
        score += 10 * len(general_author) / (max(len(self.user1_all_music), len(self.user2_all_music)) // 100 + 1)
        description += self.descriptions.get_general_authors(general_author) + "\n"

        score += 20 * len(general_title) / (max(len(self.user1_all_music), len(self.user2_all_music)) // 100 + 1)
        description += self.descriptions.get_general_titles(general_title) + "\n"

        if score >200:
            score = 200
        return score, description

    def compare_genres(self):
        g1 = self.get_best_genre(self.user1_all_music)
        g2 = self.get_best_genre(self.user2_all_music)
        if g1 == g2:
            score = 10
            description = self.descriptions.get_good_genres(g1)
        else:
            score = 0
            description = self.descriptions.get_bad_genres(g1, g2)
        return score, description

    def get_best_genre(self, music):
        g = self.get_genres(music)
        best = None
        for i in g.items():
            if best is None:
                best = i
                continue
            if len(best[1]) < len(i[1]):
                best = i
        return best[0]

    def get_genres(self, music):
        mus = {}
        for i in music:
            for j in i.genres:
                if j in mus:
                    mus[j].append(i)
                else:
                    mus[j] = [i]
        return mus

    def __have_inf(self, user):
        if user.inf["bdate"] or user.inf["home_town"] or user.inf["education"]:
            return True
        return False

    def compare_user_information(self):
        if not self.__have_inf(self.user1) and not self.__have_inf(self.user2):
            return 50, self.descriptions.get_without_inf()
        elif not self.__have_inf(self.user1):
            return 0, self.descriptions.get_without_inf(self.user1)
        elif not self.__have_inf(self.user2):
            return 0, self.descriptions.get_without_inf(self.user2)
        score = 0
        description = ""
        bd1 = self.user1.inf["bdate"]
        bd2 = self.user2.inf["bdate"]
        if bd1 and bd2:
            bd1s = bd1.split(".")
            bd2s = bd2.split(".")

            if len(bd1s) == len(bd2s) == 3:
                if bd1s[2] == bd2s[2]:
                    score += 8
                    description += self.descriptions.get_general_year(bd1s[2]) + "\n"
            if bd1s[1] == bd2s[1]:
                score += 8
                description += self.descriptions.get_general_month(bd1s[1]) + "\n"
            if bd1s[0] == bd2s[0]:
                score += 8
                description += self.descriptions.get_general_day(bd1s[0]) + "\n"
        ht1 = self.user1.inf["home_town"]
        ht2 = self.user2.inf["home_town"]
        if ht1 and ht2 and ht1 == ht2:
            score += 11
            description += self.descriptions.get_general_home_town(ht1) + "\n"

        u1 = self.user1.inf["education"]
        u2 = self.user2.inf["education"]
        if u1 and u2 and u1 == u2:
            score += 11
            description += self.descriptions.get_general_university(u1) + "\n"

        return score, description

    def compare_posts(self):
        text1 = self.vk.get_text_from_posts(self.user1.id)
        text2 = self.vk.get_text_from_posts(self.user2.id)
        tt = str.maketrans(string.punctuation, " "*len(string.punctuation))
        text1 = text1.translate(tt).replace('\n', '').lower()
        text2 = text2.translate(tt).replace('\n', '').lower()
        words1 = [i for i in text1.split() if len(i) >= 6]
        words2 = [i for i in text2.split() if len(i) >= 6]
        morph = MorphAnalyzer()
        words1 = list(map(lambda x: morph.parse(x)[0].normal_form, words1))
        words2 = list(map(lambda x: morph.parse(x)[0].normal_form, words2))
        c1 = set([i[0] for i in Counter(words1).most_common(20)])
        c2 = set([i[0] for i in Counter(words2).most_common(20)])
        general = list(c1.intersection(c2)) * 2
        score = len(general)
        description = self.descriptions.get_general_word(general) if general \
            else self.descriptions.get_not_general_word()
        return score, description

    def compare_groups(self):
        groups1 = set(self.user1.groups)
        groups2 = set(self.user2.groups)
        general = list(groups1.intersection(groups2))
        score = len(general) / (min(len(groups2), len(groups1))//10+1)
        description = self.descriptions.get_general_groups(general) if general \
            else self.descriptions.get_not_general_groups()
        description += "\n"
        return score, description

    def compare(self):
        if self.bar:
            threading.Thread(target=self._update_bar, args=[]).start()
        score = 0
        description = ""
        res = self.compare_music()
        score += res[0]
        description += res[1] + '\n'
        print("music", res[0])
        res = self.compare_posts()
        score += res[0]
        description += res[1] + '\n'
        self.progress = 80
        print("posts", res[0])
        res = self.compare_groups()
        score += res[0]
        description += res[1] + '\n'
        self.progress = 90
        print("groups", res[0])
        res = self.compare_user_information()
        score += res[0]
        description += res[1]
        print("inf", res[0])
        self.progress = 100
        self.need_update = False
        return score, description
