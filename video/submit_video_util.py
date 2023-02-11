import requests
from googleapiclient.discovery import build
from facebook_sdk import Facebook
from googleapiclient.http import MediaFileUpload
from .models import Video, Provider

from moviepy.editor import VideoFileClip

def get_video_info(video_id):
    video = Video.objects.get(id=video_id)
    video_info = []
    video_info.title = video.name
    video_info.details = video.description
    video_info.tags = video.tags.all()
    video_info.file = video.video_file

    return video_info


def convert_to_portrait(input_file, output_file):
    clip = VideoFileClip(input_file)
    clip_resized = clip.resize(height=clip.w)
    clip_resized.write_videofile(output_file)

    return clip_resized

video_details = get_video_info()
video_title = video_details['title']
video_description = video_details['details']
video_tags = video_details['tags']
video_file = video_details['file']

is_exist = Provider.objects.get(name="TikTok")
if not is_exist:
    print("TikTok does not exist.")
else:
    tik = Provider.objects.get(name="TikTok")
    # setup the TikTok client
    tiktok_api_key = tik.account_key
    tiktok_api_secret = tik.account_secret

    # upload the mobile video to TikTok
    url = "https://api.tiktok.com/v1/upload"
    data = {
        "file": open("path/to/mobile_video.mp4", "rb"),
        "api_key": tiktok_api_key,
        "api_secret": tiktok_api_secret
    }
    response = requests.post(url, data=data)
    print(response.json())


is_exist = Provider.objects.get(name="Youtube")
if not is_exist:
    print("YouTube does not exist.")
else:
    tube = Provider.objects.get(name="YouTube")
    # setup the YouTube client
    youtube = build("youtube", "v3", developerKey=tube.account_key)

    # upload the mobile video to YouTube
    video = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": video_title,
                "description": video_description,
                "tags": video_tags
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload("path/to/mobile_video.mp4", mimetype="video/mp4")
    )
    response = video.execute()
    print(response)

    # upload the desktop video to YouTube
    video = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": video_title,
                "description": video_description,
                "tags": video_tags
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_file, mimetype='video/*')
    )
    response = video.execute()
    print(response)

is_exist = Provider.objects.get(name="Facebook")
if not is_exist:
    print("Faceook does not exist.")
else:

    face = Provider.objects.get(name="Facebook")
    # setup the Facebook client
    facebook = Facebook(access_token=face.token)

    # upload the mobile video to Facebook
    video = open("path/to/mobile_video.mp4", "rb")
    response = facebook.post("/me/videos", video=video, title=video_title, description=video_description)
    print(response)

    # upload the desktop video to TikTok
    url = "https://api.tiktok.com/v1/upload"
    data = {
        "file": open("path/to/desktop_video.mp4", "rb"),
        "api_key": tiktok_api_key,
        "api_secret": tiktok_api_secret
    }
    response = requests.post(url, data=data)
    print(response.json())
