import requests
import json
from tusclient import client
from django.conf import settings

# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)

cloudlfare = None
# cloudlfare = Provider.objects.all().filter(name="CloudFlare")
"""
Set account variables for cloudflare api access
"""
if cloudlfare:
    api_url = cloudlfare.api
    account = cloudlfare.account
    token = cloudlfare.token
    auth_email = cloudlfare.auth_email
else:
    api_url = settings.CLOUDFLARE_API_URL
    account = settings.CLOUDFLARE_ACCOUNT
    token = settings.CLOUDFLARE_TOKEN
    auth_email = settings.CLOUDFLARE_AUTH_EMAIL

def verify_token():
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
    tus-upload --chunk-size 5242880 --header X-Auth-Key {api-key}
    --header X-Auth-Email {email} {path-to-video}
    https://api.cloudflare.com/client/v4/accounts/{account_id}/stream

    Formats:
    MP4, MKV, MOV, AVI, FLV, MPEG-2 TS, MPEG-2 PS, MXF, LXF, GXF, 3GP, WebM, MPG, QuickTime
    """

    my_client = client.TusClient(url=api_url  + 'stream',
                                  headers={'X-Auth-Key': token, 'X-Auth-Email': auth_email})
    logger.warning("URL:" + str(my_client.url))
    uploader = my_client.uploader(file_path=path, chunk_size=5 * 1024 * 1024, metadata={'name': file,})
    uploader.upload()
    logger.warning("STATUS:" + str(uploader) + "-" + str(uploader.url))
    if uploader.url:
        return str(uploader.url)
    else:
        return "ERROR"

    """
    files = {'upload_file': open(path,'rb')}
    resp = requests.post(api_url + 'stream',
                    headers = {'Authorization': token, 'X-Auth-Email': auth_email},
                    files=files)

    logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
    return resp.content
    """

def check_encoding(video_id):
    """
    curl 'https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/{video-id}' \
        -H 'X-Auth-Email: {email}' \
        -H 'X-Auth-Key: {api-key}' \
        -H 'Content-Type: application/json'
    """
    resp = requests.get(api_url + 'stream/' + video_id ,
                    headers = {'X-Auth-Key': token, 'X-Auth-Email': auth_email})
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
    resp = requests.get(api_url + 'stream/' + video_id + '/embed',
                    headers = {'X-Auth-Key': token, 'X-Auth-Email': auth_email})
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return str(resp.status_code)
    else:
        return str(resp.content['embed_code'])


def get_details(video_id):
    """
    curl -X GET "https://api.cloudflare.com/client/v4/accounts/023e105f4ecef8ad9ca31a8372d0c353/stream/ea95132c15732412d22c1476fa83f27a" \
     -H "X-Auth-Email: user@example.com" \
     -H "X-Auth-Key: c2547eb745079dac9320b638f5e225cf483cc5cfdda41" \
     -H "Content-Type: application/json"
    """
    resp = requests.get(api_url + 'stream/' + video_id,
                    headers = {'X-Auth-Key': token, 'X-Auth-Email': auth_email})
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return resp.status_code
    else:
        return json.loads(resp.content)

def search_video(name):
    resp = requests.get('api_url' + 'accounts/' + account_id + '/media?search=' + name,
                        data = json.dumps(data),
                        headers = {'X-Auth-Key': token, 'X-Auth-Email': auth_email})
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return str(resp.status_code)
    else:
        return json.loads(resp.content)

def delete_video(video_id):
    resp = requests.delete(api_url + 'stream/' + video_id,
                    headers = {'X-Auth-Key': token, 'X-Auth-Email': auth_email})
    if resp.status_code != 200:
        logger.warning("ERROR:" + str(resp.status_code) + "-" + str(resp.content))
        return str(resp.status_code)
    else:
        return str(resp.status_code)
