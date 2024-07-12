from decouple import config

from youtube_func import move_playlist_videos_to_archive

move_playlist_videos_to_archive(
    source_playlist_id=config("yt_source_pl_id"),
    archive_playlist_id=config("yt_archive_pl_id"),
)
