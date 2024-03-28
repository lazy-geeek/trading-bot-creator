import os
import pathlib
from tqdm import tqdm
from datetime import datetime
import shutil

path = pathlib.Path.cwd() / f'transcripts/'

def move_existing_files_to_archive():
    # if path contains files, move them to archive folder
    files = os.listdir(path)
    if files:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(path / timestamp, exist_ok=True)        
        for file in tqdm(files, desc="Moving files to archive", total=len(files)):
            os.rename(path / file, path / timestamp / file)            

def save_transcipt_to_file(transcript,filename):
    filename = filename.replace(" ", "_")
    filename = filename.replace("/", "_")
    file_path = path / f'{filename}.txt'
    with open(file_path, 'w') as f:
        f.write(transcript)
        
def save_transcipts_to_file(transcripts):
    move_existing_files_to_archive()
    for transcript in tqdm(transcripts, desc="Saving transcripts", total=len(transcripts)):
        save_transcipt_to_file(transcript["text"],transcript["name"])


