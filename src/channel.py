import json
import os

from googleapiclient.discovery import build
from config import CHANNEL_DATA

class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel = self.youtube.channel().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = self.channel_data['items'][0]['snippet']['title']
        self.description = self.channel_data['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"

        self.subs_count = self.channel_data['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_data['items'][0]['statistics']['videoCount']
        self.views_count = self.channel_data['items'][0]['statistics']['subscriberCount']

        self.new_data = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subs_count': self.subs_count,
            'video_count': self.video_count,
            'views_count': self.views_count,
        }

    def __str__(self):
        return f"{self.title}({self.url})"

    def __add__(self, other):
        return int(self.subs_count) + int(other.subs_count)

    def __sub__(self, other):
        return int(self.subs_count) - int(other.subs_count)

    def __gt__(self, other):
        return int(self.subs_count) > int(other.subs_count)

    def __ge__(self, other):
        return int(self.subs_count) >= int(other.subs_count)

    def __lt__(self, other):
        return int(self.subs_count) < int(other.subs_count)

    def __le__(self, other):
        return int(self.subs_count) <= int(other.subs_count)

    def __eq__(self, other):
        return int(self.subs_count) == int(other.subs_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(self.channel)


    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file_name):
        json_data = json.dumps(self.new_data, ensure_ascii=False)

        with open(f"../Data/{file_name}", 'w', encoding='windows-1251') as file:
            file.write(json_data)

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))