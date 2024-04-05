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

def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en','de'])        
        return ' '.join([t['text'] for t in transcript.fetch()])
    except Exception as e:
        return None

def get_playlist_transcripts(playlist_url):
    transcripts = []

    playlist = Playlist(playlist_url)
    
    for video in tqdm(playlist.videos,desc="Downloading transcripts",total=len(playlist.videos)):   
        
        text = ""
        text = get_video_transcript(video.video_id)        
        if text is not None:
            name = video.title
            transcript = {}   
            transcript["text"] = text
            transcript["name"] = name   
            transcripts.append(transcript)
    
    move_videos_to_archive()
        
    return transcripts

def move_videos_to_archive():    
    source_playlist_id = config("yt_source_pl_id")
    archive_playlist_id = config("yt_archive_pl_id")
    
    client_secrets_file = "client_secret.json"

    '''
    # Get credentials and create an API client    
    
    credentials = Credentials.from_authorized_user_file(client_secrets_file)
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.run_local_server(port=8080)
    credentials = flow.credentials
    '''
    
    youtube = create_service(client_secrets_file, 'youtube', 'v3', scopes)
    
    # Remove video from source playlist
    
    response = youtube.playlistItems().list(
        part=['id','contentDetails'],
        playlistId=source_playlist_id,
    ).execute()    
    
    videos = response['items']
    
    for video in videos:    
    
        print()
    
        # Add video to target playlist
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": archive_playlist_id,
                    "position": 0,
                    "resourceId": {                        
                        "kind": "youtube#video",
                        "videoId": video['contentDetails']['videoId'],
                    }
                }
            }
        ).execute()
        
        youtube.playlistItems().delete(        
            id=video['id']            
        ).execute()
        
        print(f"Video (ID: {video['id']}) moved from playlist (ID: {source_playlist_id}) to playlist (ID: {archive_playlist_id})")

move_videos_to_archive()