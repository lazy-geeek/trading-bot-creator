#TODO   Integrate google_apis.py in youtube.py 

#TODO   Get summary from transcript
#TODO   Run youtube transcription as standalone service
#TODO   Save files in ftp path

from decouple import config

from youtube import get_playlist_transcripts
from file_mgt import save_texts_to_file

playlist_url = config("yt_source_pl_url")
transcripts = get_playlist_transcripts(playlist_url)
save_texts_to_file(texts=transcripts,foldername="transcripts")
