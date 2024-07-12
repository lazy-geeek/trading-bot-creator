from decouple import config

from youtube_func import get_playlist_transcripts
from ftp_mgt import save_texts_to_file

foldername = "transcripts"

transcripts = get_playlist_transcripts(playlist_url=config("yt_source_pl_url"))
save_texts_to_file(texts=transcripts, foldername=foldername)
