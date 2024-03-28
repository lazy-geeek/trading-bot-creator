from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
from tqdm import tqdm

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
        
    return transcripts



