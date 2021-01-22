import requests
import json
from tusclient import client
from django.conf import settings
from video.models import Provider 

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
