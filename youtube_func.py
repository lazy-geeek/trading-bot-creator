from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
from tqdm import tqdm
from google_apis import create_service
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from decouple import config
from pprint import pprint

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
client_secrets_file = "client_secret.json"


def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(["en", "de"])
        return " ".join([t["text"] for t in transcript.fetch()])
    except Exception as e:
        return None


def get_playlist_transcripts(playlist_url):
    transcripts = []

    playlist = Playlist(playlist_url)

    print("Number of videos in playlist: %s" % len(playlist.videos))

    for video in tqdm(
        playlist.videos, desc="Downloading transcripts", total=len(playlist.videos)
    ):

        # TODO Check if video still does exist. If not remove from playlist

        text = ""
        text = get_video_transcript(video.video_id)
        if text is not None:
            name = video.title
            transcript = {}
            transcript["text"] = text
            transcript["name"] = name
            transcripts.append(transcript)

    return transcripts


def all_videos_from_playlist(playlist_id):
    youtube = None
    videos = []
    next_page_token = None

    try:
        youtube = create_service(client_secrets_file, "youtube", "v3", scopes)
    except Exception as e:
        print(e)

    while True:
        request = youtube.playlistItems().list(
            part=["id", "contentDetails"],
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        )
        response = request.execute()

        for item in response["items"]:
            videos.append(item)

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break  # No more pages

    return videos, youtube


def move_playlist_videos_to_archive(source_playlist_id, archive_playlist_id):
    videos, youtube = all_videos_from_playlist(source_playlist_id)

    for video in tqdm(videos, desc="Archiving videos", total=len(videos)):

        # Add video to target playlist
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": archive_playlist_id,
                    "position": 0,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video["contentDetails"]["videoId"],
                    },
                }
            },
        ).execute()

        # Remove video from source playlist
        youtube.playlistItems().delete(id=video["id"]).execute()

        # print(f"Video (ID: {video['id']}) moved from playlist (ID: {source_playlist_id}) to playlist (ID: {archive_playlist_id})")
