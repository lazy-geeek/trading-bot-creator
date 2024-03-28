#TODO   After transribing, move video to archive playlist
#TODO   Get summary from transcript

from decouple import config

from youtube import get_playlist_transcripts
from transcript_mgt import save_transcipts_to_file

playlist_url = config("yt_source_pl")
transcripts = get_playlist_transcripts(playlist_url)
save_transcipts_to_file(transcripts)
