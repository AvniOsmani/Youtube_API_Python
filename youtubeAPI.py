#python3 youtubeAPI.py
#.bashrc

import os
from googleapiclient.discovery import build

api_key = os.environ.get('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
        part='statistics',
        forUsername='phshockey12'
    )

response = request.execute()

print(response)
