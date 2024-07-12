from ftplib import FTP, error_perm
from decouple import config

try:

    # Step 1: Connect to the FTP server
    ftp = FTP(config("ftp_url"))

    # Step 2: Login to the FTP server
    ftp.login(user=config("ftp_user"), passwd=config("ftp_pass"))

    # iterate 3 time
    for i in range(3):

        foldername = "transcripts"

        if ftp.pwd() == "/":
            if not foldername in ftp.nlst():
                ftp.mkd(foldername)

        if not ftp.pwd() == f"/{foldername}":
            ftp.cwd(foldername)

        print(f"Current directory: {ftp.pwd()}")

except error_perm as e:
    print(f"FTP error: {e}")
except Exception as e:
    print(f"Error: {e}")
