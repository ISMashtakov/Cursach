from yandex_music.client import Client
from yandex_music.client import Track


class Music:
    def __init__(self):
        self.name = None
        self.author = None
        self.genres = []
        self.duration = None
        self.year = None


class YaMusic:
    def __init__(self):
        self.client = Client()

    def get_inf_for_song(self, title):
        song = self.client.search(title).best.result
        if type(song) is not Track:
            return None

        music = Music()
        music.duration = song.duration_ms
        music.name = song.title
        music.author = [a.name for a in song.artists]
        music.year = song.albums[0].year or song.albums[0].release_date if song.albums else None
        music.genres = [a.genre for a in song.albums if a.genre]
        return music


