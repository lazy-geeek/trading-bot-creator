from ftplib import FTP, error_perm
from io import BytesIO
from decouple import config
from tqdm import tqdm
from werkzeug.utils import secure_filename


try:

    # Step 1: Connect to the FTP server
    ftp = FTP(config("ftp_url"))

    # Step 2: Login to the FTP server
    ftp.login(user=config("ftp_user"), passwd=config("ftp_pass"))

except error_perm as e:
    print(f"FTP error: {e}")
except Exception as e:
    print(f"Error: {e}")


def save_text_to_file(text, filename, foldername):
    try:
        # current ftp foldername

        if ftp.pwd() == "/":
            if not foldername in ftp.nlst():
                ftp.mkd(foldername)

        if not ftp.pwd() == f"/{foldername}":
            ftp.cwd(foldername)

        filename = f"{secure_filename(filename)}.txt"

        # Step 4: Create and upload the text file in memory
        bio = BytesIO(text.encode("utf-8"))
        ftp.storbinary(f"STOR {filename}", bio)

    except Exception as e:
        print(f"Error: {e}")


def save_texts_to_file(texts, foldername):
    # move_existing_files_to_timestamp_archive(foldername)
    for text in tqdm(texts, desc="Saving texts to file", total=len(texts)):
        save_text_to_file(text["text"], text["name"], foldername)


"""

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
        


def get_text_from_file(foldername):
    path = pathlib.Path.cwd() / f'{foldername}/'
    #Get first txt file from folder and return its content
    files = [f for f in os.listdir(path) if f.endswith(".txt")]
    if files:
        with open(path / files[0], 'r') as f:
            return f.read()
            

"""
