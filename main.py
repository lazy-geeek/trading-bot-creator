#TODO   Google Youtube Quota Exceeded
#TODO   Get summary from transcript
#TODO   Run youtube transcription as standalone service
#TODO   Save files in ftp path

from decouple import config

from youtube import get_playlist_transcripts,move_playlist_videos_to_archive
from file_mgt import save_texts_to_file

#transcripts = get_playlist_transcripts(playlist_url=config("yt_source_pl_url"))
#save_texts_to_file(texts=transcripts,foldername="transcripts")
move_playlist_videos_to_archive(source_playlist_id=config("yt_source_pl_id"),archive_playlist_id=config("yt_archive_pl_id"))
