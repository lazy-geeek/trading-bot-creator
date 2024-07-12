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


def get_texts_from_folder(foldername):

    texts = []

    ftp.cwd(foldername)

    filenames = ftp.nlst()
    filenames = filenames[:5]

    # open all files with ending .txt in folder

    for filename in tqdm(
        filenames, desc="Reading files from FTP", total=len(filenames)
    ):
        if filename.endswith(".txt"):
            bio = BytesIO()
            ftp.retrbinary(f"RETR {filename}", bio.write)
            bio.seek(0)
            text = {}
            text["name"] = filename.replace(".txt", "")
            text["text"] = bio.getvalue().decode("utf-8")
            texts.append(text)

    if texts:
        return texts
    else:
        return None

    # open file with ftplib

    # read file

    # save file

    # close file
