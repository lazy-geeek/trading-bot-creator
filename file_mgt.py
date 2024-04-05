import os
import pathlib
from tqdm import tqdm
from datetime import datetime
from werkzeug.utils import secure_filename

def move_existing_files_to_timestamp_archive(foldername):
    # if path contains files, move them to archive folder
    path = pathlib.Path.cwd() / f'{foldername}/'
    if not os.path.exists(path):
        os.makedirs(path)
    files = os.listdir(path)
    if files:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(path / timestamp, exist_ok=True)        
        for file in tqdm(files, desc="Moving files to archive", total=len(files)):
            os.rename(path / file, path / timestamp / file)            

def save_text_to_file(text,filename,foldername):
    path = pathlib.Path.cwd() / f'{foldername}/'
    if not os.path.exists(path):
        os.makedirs(path)
    filename = secure_filename(filename)    
    file_path = path / f'{filename}.txt'
    with open(file_path, 'w') as f:
        f.write(text)
        
def save_texts_to_file(texts,foldername):    
    move_existing_files_to_timestamp_archive(foldername)
    for text in tqdm(texts, desc="Saving texts to file", total=len(texts)):
        save_text_to_file(text["text"],text["name"],foldername)

def get_text_from_file(foldername):
    path = pathlib.Path.cwd() / f'{foldername}/'
    #Get first txt file from folder and return its content
    files = [f for f in os.listdir(path) if f.endswith(".txt")]
    if files:
        with open(path / files[0], 'r') as f:
            return f.read()
