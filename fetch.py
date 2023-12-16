# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

from dataclasses import dataclass, field
from datetime import datetime
import os
import isodate
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

api_service_name = "youtube"
api_version = "v3"
# os.environ["API_KEY"] = ""
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=os.environ["API_KEY"])
# Video(**{'videoId': 'HwKjtJ1unlQ', 'videoPublishedAt': '2022-04-01T14:00:16Z'})


@dataclass
class Video:
    videoId: str
    videoPublishedAt: str
    _video: dict = None  # type: ignore

    @property
    def published_date(self) -> datetime:
        return datetime.strptime(
            self.videoPublishedAt,
            "%Y-%m-%dT%H:%M:%SZ")

    @property
    def video(self):
        if (self._video is None):
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=self.videoId
            )
            self._video = request.execute()['items'][0]
        return self._video

    @property
    def duration(self):
        return isodate.parse_duration(
            self.video['contentDetails']['duration']).total_seconds()


@dataclass
class PlayList:
    list_id: str

    @property
    def videos(self):
        response = self.fetch_videos()
        has_more = True
        while (has_more):
            for element in response["items"]:
                try:
                    yield Video(**element['contentDetails'])
                except TypeError:
                    pass
            if ("nextPageToken" in response):
                response = self.fetch_videos(token=response["nextPageToken"])
            else:
                has_more = False

    def fetch_videos(self, token=None):
        request = youtube.playlistItems().list(
            part="contentDetails",
            maxResults=50,
            playlistId="PLjJNtVylHOh_eq3L9z5NQbdbNoHIXnDhm",
            pageToken=token
        )
        response = request.execute()
        return response


result = [
    (video.published_date, video.duration)
    for video in PlayList("PLjJNtVylHOh_eq3L9z5NQbdbNoHIXnDhm").videos]

