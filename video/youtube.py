import requests
import json
from tusclient import client
from django.conf import settings
from video.models import Provider, Video
from django.shortcuts import render, redirect
from django.conf import settings


# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)

"""
Set account variables for youtube api access
"""
youtube = Provider.objects.filter(name="YouTube").first()
if youtube:
    api_url = youtube.api_url
    account_key = youtube.account_key
else:
    api_url = settings.YOUTUBE_API_URL
    account_key = settings.YOUTUBE_API_KEY
def upload_video(file, path):
    # Set Authorization headers if it is required
    # by the tus server.
    """
    curl --request POST \
      'https://www.googleapis.com/youtube/v3/videos?key=[YOUR_API_KEY]' \
      --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
      --header 'Accept: application/json' \
      --header 'Content-Type: application/json' \
      --data '{}' \
      --compressed

    Formats:
    MP4, MKV, MOV, AVI, FLV, MPEG-2 TS, MPEG-2 PS, MXF, LXF, GXF, 3GP, WebM, MPG, QuickTime
    """
    my_client = client.TusClient(url=api_url  + 'account_key',
                                  headers={'Authorization: Bearer ' + token})
    logger.warning("URL:" + str(my_client.url))
    uploader = my_client.uploader(file_path=path, chunk_size=5 * 1024 * 1024, metadata={'name': file,})
    uploader.upload()
    logger.warning("STATUS:" + str(uploader) + "-" + str(uploader.url))
    if uploader.url:
        return str(uploader.url)
    else:
        return "ERROR"

def get_video():
    """
    curl \
      'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=Ks-_Mh1QhMc&key=[YOUR_API_KEY]' \
      --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
      --header 'Accept: application/json' \
      --compressed
    """
    resp = requests.get(api_url + 'account_key' + '&' + 'part=snippet%2CcontentDetails%2Cstatistics&id=Ks-_Mh1QhMc',
                    headers={'Authorization: Bearer ' + token})
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return resp.status_code
    else:
        return json.loads(resp.content)


def update_video():
    """
    curl --request PUT \
    'https://www.googleapis.com/youtube/v3/videos?key=[YOUR_API_KEY]' \
    --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --data '{}' \
    --compressed
    """

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

def upload_video_post(file):

    get_video = Video.objects.get(pk=file)

    from google.oauth2.service_account import Credentials

    # Build the credentials object using the service account key JSON file
    creds = Credentials.from_service_account_file(settings.GOOGLE_APPLICATION_CREDENTIALS)

    try:
        # Build the YouTube API client
        youtube = build("youtube", "v3", credentials=creds)

        # Get the path to a file uploaded to the media directory
        file_path = get_video.video_file.path

        # Get the video file and meta data
        video_file = file_path
        video_name = get_video.name
        video_description = get_video.description

        import os

        if not os.path.exists(video_file):
            print("The file does not exist at the specified path: {}".format(video_file))

        # Create the MediaFileUpload object
        media = MediaFileUpload(video_file, chunksize=1024*1024, resumable=True)

        # Create the video
        video = youtube.videos().insert(
            part='snippet,status',
            body={
                'snippet': {
                    'title': video_name,
                    'description': video_description,
                    'categoryId': '22'
                },
                'status': {
                    'privacyStatus': 'private',
                    },
            },
            media_body=media
        ).execute()
        return redirect(f'https://www.youtube.com/watch?v={video["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return render('500.html', {'error': 'Invalid platform'})

