import logging
import json
import os

from yandex_music.client import Client
from yandex_music.client import Track
from yandex_music.base import logger


all_genres = {
        "rnb": {"I": "RNB", "R": "RNB", "V": "RNB"},
        "rusrock": {"I": "русский рок", "R": "русского рока", "V": "русский рок"},
        "videogame": {"I": "музыка из игр", "R": "музыки из игр", "V": "музыку из игр"},
        "local-indie": {"I": "местное инди", "R": "местного инди", "V": "местное инди"},
        "folk": {"I": "народная музыка", "R": "народной музыки", "V": "народную музыку"},
        "metal": {"I": "метал", "R": "метала", "V": "метал"},
        "rusrap": {"I": "русский реп", "R": "русского репа", "V": "русский реп"},
        "pop": {"I": "попса", "R": "попсы", "V": "попсу"},
        "electronics": {"I": "электронная музыка", "R":  "электронной музыки", "V": "электронную музыку"},
        "hardrock": {"I": "тяжёлый рок", "R": "тяжёлого рока", "V": "тяжёлый рок"},
        "indie": {"I": "инди", "R": "инди", "V": "инди"},
        "tvseries": {"I": "музыка из сериалов", "R": "музыки из сериалов", "V": "музыку из сериалов"},
        "rock": {"I": "рок", "R": "рока", "V": "рок"},
        "modern": {"I": "современная музыка", "R": "современной музыки", "V": "современную музыку"},
        "vocal": {"I": "вокал", "R": "вокала", "V": "вокал"},
        "foreignrap": {"I": "иностранный реп", "R": "иностранного репа", "V": "иностранный реп"},
        "punk": {"I": "панк", "R": "панка", "V": "панк"},
        "posthardcore": {"I": "хардкор", "R": "хардкора", "V": "хардкор"},
        "ruspop": {"I": "русская попса", "R": "русской попсы", "V": "русскую попсу"},
        "musical": {"I": "мюзикл", "R": "мюзиклов", "V": "мюзикл"},
        "rusestrada": {"I": "русская эстрадная музыка", "R": "русской эстрадной музыки", "V": "русскую эстрадную музыку"},
        "alternative": {"I": "альтернативная музыка", "R": "альтернативной музыки", "V": "альтернативную музыку"},
        "prog": {"I": "прогрессивная музыка", "R": "прогрессивной музыки", "V": "прогрессивную музыку "},
        "classicmetal": {"I": "классический метал", "R": "классического метала", "V": "классический метал"},
        "trance": {"I": "транс", "R": "транса", "V": "транс"},
        "films": {"I": "музыка из фильмов", "R": "музыки из фильмов", "V": "музыку из фильмов"},
        "soundtrack": {"I": "саундтреки", "R": "саундтреков", "V": "саундтреки"},
        "foreignbard": {"I": "иностранная авторская песня", "R": "иностранной авторской песни", "V": "иностранную авторскую песню"},
        "rusbards": {"I": "русская авторская песня", "R": "русской авторской песни", "V": "русскую авторскую песню"},
        "dance": {"I": "танцевальная музыка", "R": "танцевальной музыки", "V": "танцевальную музыку"},
        "country": {"I": "кантри", "R": "кантри", "V": "кантри"},
        "relax": {"I": "музыка для раслабления", "R": "музыки для раслабления", "V": "музыку для расслабления "},
        "numetal": {"I": "ню-метал", "R": "ню-метала", "V": "метал"},
        "house": {"I": "хаус", "R": "хауса", "V": "хаус"},
        "forchildren": {"I": "десткая музыка", "R": "детской музыки", "V": "детскую музыку"},
        "animated": {"I": "музыка из мультиков", "R": "музыки из мультфильмов", "V": "музыку из мультфильмов"},
        "estrada": {"I": "эстрадная музыка", "R": "эстрадной музыки", "V": "эстрадную музыку"},
        "stonerrock": {"I": "стоунер-рок", "R": "стоунер-рока", "V": "стоунер-рок"},
        "ukrrock": {"I": "украинский рок", "R": "украинского рока", "V": "украинский рок"},
        "rnr": {"I": "современный ар-н-би", "R": "современного ар-н-би", "V": "современный ар-н-би"},
        "rusfolk": {"I": "русская народная музыка", "R": "русской народной музыки", "V": "русскую народную музыку"},
        "shanson": {"I": "шансон", "R": "шансона", "V": "шансон"},
        "newwave": {"I": "новая волна", "R": "новой волны ", "V": "новую волну"},
        "blues": {"I": "блюз", "R": "блюза", "V": "блюз"},
        "epicmetal": {"I": "эпичный метал", "R": "эпичного метала", "V": "эпичный метал"},
        "newage": {"I": "нью-эйдж", "R": "нью-эйдж", "V": "нью-эйдж"},
        "classical": {"I": "классическая музыка", "R": "классической музыки", "V": "классическую музыку"},
        "society": {"I": "социальная музыка", "R": "социальной музыки", "V": "социальная музыка"},
        "podcasts": {"I": "подкасты", "R": "подкастов", "V": "подкасты"},
        "latinfolk": {"I": "латинская народная музыка", "R": "латинской народной музыки", "V": "латинскую народную музыку"},
        "comedypodcasts": {"I": "юмористический подкасты", "R": "юмористических подкастов", "V": "юмористический подкасты"},
        "disco": {"I": "диско", "R": "диско", "V": "диско"},
        "fairytales": {"I": "сказки", "R": "сказок", "V": "сказки"},
        "extrememetal": {"I": "экстремальный метал", "R": "экстремального метала", "V": "экстремальный метал"},
        "ska": {"I": "ска", "R": "ска", "V": "ска"},
        "folkrock": {"I": "русский народный рок", "R": "русского народного рока", "V": "русский народный рок"},
        "kpop": {"I": "kpop", "R": "kpop", "V": "kpop"},
        "reggae": {"I": "регги ", "R": "регги ", "V": "регги"},
        "soul": {"I": "душевная музыка", "R": "душевной музыки", "V": "душевную музыку"},
        "dnb": {"I": "драм-н-бейс", "R": "драм-н-бейса", "V": "драм-н-бейс"},
        "industrial": {"I": "индастриал", "R": "индастриала", "V": "индастриал"},
        "allrock": {"I": "рок", "R": "рока", "V": "рок"},
        "dub": {"I": "даб", "R": "даба", "V": "даб"},
        "hardcore": {"I": "хардкор", "R": "хардкора", "V": "хардкор"},
        "progmetal": {"I": "метал", "R": "метала", "V": "метал"},
        "dubstep": {"I": "дабстеп", "R": "дабстепа", "V": "дабстеп"},
        "folkmetal": {"I": "традиционный метал", "R": "традиционного метала", "V": "традиционный метал"},
        "jazz": {"I": "джаз", "R": "джаза", "V": "джаз"},
        "rap": {"I": "реп", "R": "репа", "V": "реп"},
        "sport": {"I": "спортивная музыка", "R": "спортивной музыки", "V": "спортивную музыку"},
        "techno": {"I": "техно", "R": "техно", "V": "техно"},
    }


class Music:
    def __init__(self):
        self.name = None
        self.author = None
        self.genres = []
        self.duration = None
        self.year = None

    def __str__(self):
        return "{} - {}".format(self.author, self.name)

    def to_json(self):
        return {
            "name": self.name,
            "author": self.author,
            "genres": self.genres,
            "duration": self.duration,
            "year": self.year
        }

    @staticmethod
    def from_json(dic):
        obj = Music()
        obj.name = dic["name"]
        obj.author = dic["author"]
        obj.genres = dic["genres"]
        obj.duration = dic["duration"]
        obj.year = dic["year"]
        return obj


class YaMusic:

    cache_path = "ya_cache.json"

    def __init__(self):
        logger.level = logging.ERROR
        self.client = Client()
        self.cache = {}
        self.load_cache()
        self.i = 0

    def load_cache(self):
        if not os.path.exists(self.cache_path):
            return
        with open(self.cache_path, "r") as file:
            d = json.load(file)
        for key, value in d.items():
            self.cache[key] = Music.from_json(value)

    def save_cache(self):
        d = {}
        for key, value in self.cache.items():
            d[key] = value.to_json()
        with open(self.cache_path, "w") as file:
            json.dump(d, file)

    def get_song(self, name, author):
        title = "{} - {}".format(author, name)
        song = self.cache.get(title, None)
        if song:
            return song

        self.i += 1
        if self.i > 50:
            self.save_cache()
            self.i = 0

        song = self.client.search(title).best
        if song is None or type(song.result) is not Track:
            music = Music()
            music.name = name
            music.author = [author]
            self.cache[title] = music
            return music
        song = song.result

        music = Music()
        music.duration = song.duration_ms
        music.name = song.title
        music.author = [a.name for a in song.artists]
        music.year = song.albums[0].year or song.albums[0].release_date if song.albums else None
        music.genres = [a.genre for a in song.albums if a.genre]
        for i in music.genres:
            if i not in all_genres:
                print(i)
        self.cache[title] = music
        return music


