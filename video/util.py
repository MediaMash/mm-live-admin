import requests
import json
from tusclient import client
from django.conf import settings
from .models import Provider
# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)

"""
Set account variables for cloudflare api access
https://developers.cloudflare.com/api/operations/stream-videos-list-videos
"""
def setup():
    cloudflare = Provider.objects.all().filter(name="Internal").first()
    if cloudflare:
        api_url = cloudflare.api_url
        account = cloudflare.account_key
        token = cloudflare.token
        auth_email = cloudflare.auth_email
    else:
        api_url = settings.CLOUDFLARE_API_URL
        account = settings.CLOUDFLARE_ACCOUNT
        token = settings.CLOUDFLARE_TOKEN
        auth_email = settings.CLOUDFLARE_AUTH_EMAIL
    return api_url,account,token,auth_email

def verify_token():
    api_url,account,token,auth_email=setup()
    resp = requests.get(api_url + 'user/tokens/verify',
                    headers = {'Authorization': token, 'X-Auth-Email': auth_email})
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return str(resp.status_code)
    else:
        return str(resp.status_code)

def upload_video(file, path):
    # Set Authorization headers if it is required
    # by the tus server.
    """
    Formats:
    MP4, MKV, MOV, AVI, FLV, MPEG-2 TS, MPEG-2 PS, MXF, LXF, GXF, 3GP, WebM, MPG, QuickTime
    """

    api_url,account,token,auth_email=setup()

    print("url: " + api_url + account + '/stream')
    
    # Create a new tus client
    my_client = client.TusClient(url=api_url + account + '/stream?direct_user=true',
                              headers={'Authorization': 'Bearer ' + token })

    # Open the video file
    with open(path, 'rb') as file:
        # Start the upload
        uploader = my_client.uploader(path, chunk_size=52428800, retries=5)

        # Start the upload
        uploader.upload()

        response = uploader.url

        video_url = response[:response.find('?', 0)]
        
    return video_url
   
    
def check_encoding(video_id):
    # https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/{video-id}
    api_url,account,token,auth_email=setup()
    resp = requests.get(api_url + account + '/stream/' + video_id ,
                    headers={'Authorization': 'Bearer ' + token })
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return str(resp.status_code)
    else:
        return str(resp.content['status'])

def get_embed_code(video_id):
    """
    curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/{video-id}/embed" \
        -H 'X-Auth-Email: {email}' \
        -H 'X-Auth-Key: {api-key}' \
        -H 'Content-Type: application/json'
    """
    api_url,account,token,auth_email=setup()
    resp = requests.get(api_url + account + '/stream/' + video_id + '/embed',
                    headers={'Authorization': 'Bearer ' + token })
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return str(resp.status_code)
    else:
        return str(resp.content['embed_code'])


def get_details(video_id):
    # https://api.cloudflare.com/client/v4/accounts/023e105f4ecef8ad9ca31a8372d0c353/stream/ea95132c15732412d22c1476fa83f27a
    api_url,account,token,auth_email=setup()
    print(api_url + account + '/stream/' + video_id)
    resp = requests.get(api_url + account + '/stream/' + video_id,
                    headers={'Authorization': 'Bearer ' + token })
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return resp.status_code
    else:
        return json.loads(resp.content)

def search_video(name):
    api_url,account,token,auth_email=setup()
    resp = requests.get(api_url + account  + '/media?search=' + name,
                        headers={'Authorization': 'Bearer ' + token })
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return str(resp.status_code)
    else:
        return json.loads(resp.content)

def delete_video(video_id):
    api_url,account,token,auth_email=setup()
    resp = requests.delete(api_url + account + '/stream/' + video_id,
                    headers={'Authorization': 'Bearer ' + token })
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return str(resp.status_code)
    else:
        return str(resp.status_code)

def list_vidoes():
    # https://api.cloudflare.com/client/v4/accounts/{account_identifier}/stream
    api_url,account,token,auth_email=setup()
    resp = requests.get(api_url + account  + '/stream',
                        headers={'Authorization': 'Bearer ' + token })
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return str(resp.status_code)
    else:
        return str(resp)
