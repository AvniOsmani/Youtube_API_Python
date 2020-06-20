#python3 youtubeAPI.py
#.bashrc
#the playlistID is all of the charaters after the 'list=' in the playlist's URL
#example playlistID: PLCvqKltYUg-L4bKc-F_y-2idxHrARegPY

import os
import re
from datetime import timedelta
from googleapiclient.discovery import build

api_key = os.environ.get('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

playlistURL = input("Enter the playlistID from the URL of the playlist you want to see the total duration: ")

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0

nextPageToken = None
while True:
    playlist_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlistURL,
            maxResults=50,
            pageToken=nextPageToken
        )

    playlist_response = playlist_request.execute()

    video_IDs = []

    for item in playlist_response['items']:
        video_IDs.append(item['contentDetails']['videoId'])

    video_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(video_IDs)
    )

    video_response = video_request.execute()

    for item in video_response['items']:
        duration = item['contentDetails']['duration']

        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        video_seconds = timedelta(
                hours = hours,
                minutes = minutes,
                seconds = seconds
        ).total_seconds()

        total_seconds += video_seconds

    nextPageToken = playlist_response.get('nextPageToken')

    if not nextPageToken:
        break

total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

if hours<10: hours = '0' + str(hours)
if minutes<10: minutes = '0' + str(minutes)
if seconds<10: seconds = '0' + str(seconds)
print("Total duration of playlist")
print("HH:MM:SS")
print(f'{hours}:{minutes}:{seconds}')
