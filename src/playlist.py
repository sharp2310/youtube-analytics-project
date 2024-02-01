import os
from datetime import datetime, timedelta

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class PlayList:
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id) -> None:
        self.__playlist_id = playlist_id
        playlist_response = (self.youtube.playlists().
                             list(id=playlist_id,
                                  part='snippet,contentDetails',
                                  maxResults=50).execute())

        self.title = playlist_response['items'][0]['snippet']['title']
        self.url = (f"https://www.youtube.com/playlist?list="
                    f"{self.__playlist_id}")

    @property
    def total_duration(self):
        """Возвращает объект класса datetime.timedelta
        с длительность плейлиста"""
        vid_resp = self._get_videos()
        duration = timedelta(hours=0, minutes=0, seconds=0)
        for video in vid_resp:
            raw_duration = video['contentDetails']['duration']
            if "S" in raw_duration:
                format_dtm = "PT%MM%SS"
            else:
                format_dtm = "PT%MM"
            fixed_duration = datetime.strptime(raw_duration, format_dtm)
            timedelta_duration = timedelta(hours=fixed_duration.hour,
                                           minutes=fixed_duration.minute,
                                           seconds=fixed_duration.second)
            duration += timedelta_duration
        return duration

    def show_best_video(self) -> str:
        """Возвращает ссылку на самое популярное видео из плейлиста
        (по количеству лайков)"""
        vid_resp = self._get_videos()
        stats = []
        for video in vid_resp:
            stat = {"id": video['id'],
                    "like_count": video["statistics"]["likeCount"]}
            stats.append(stat)
        max_likes = max(stats, key=lambda x: x["like_count"])
        vid_id = max_likes["id"]
        url = f"https://youtu.be/{vid_id}"
        return url

    def _get_videos(self):
        playlist_videos = (self.youtube.playlistItems().
                           list(playlistId=self.__playlist_id,
                                part='contentDetails').execute())
        video_ids: list[str] = [video['contentDetails']['videoId']
                                for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)).execute()

        return video_response['items']