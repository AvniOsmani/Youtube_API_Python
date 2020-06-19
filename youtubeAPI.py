#python3 youtubeAPI.py
#.bashrc
#phshockey12

import os
from googleapiclient.discovery import build

api_key = os.environ.get('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

channel_username = input("Enter channel username to lookup statisitics: ")

request = youtube.channels().list(
        part='statistics',
        forUsername=channel_username
    )

response = request.execute()

print(response)
