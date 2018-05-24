from os import path, listdir, makedirs
from shutil import copyfile
from time import time, localtime, strftime, sleep
from datetime import datetime

"""
automatic DSR backup file creation
(1) creates backups upon start
(2) creates backups every MINUTES_X minutes defined below. Default: 5
note: the documents folder has to be set as FOLDER_documents below. Default: 'documents'
note: auto save only for files which have been modified in the last 10 minutes
note: should be compiled using PyInstaller
"""

# variables
# insert the name of the windows documents folder
# depends either on locale (by default) or user setting
FOLDER_documents = "documents"
MINUTES_X = 5


# Constants
PATH_UserFolder = path.expandvars("%userprofile%")
PATH_DSR = path.join(PATH_UserFolder, FOLDER_documents, "NBGI", "DARK SOULS REMASTERED")
PATH_DSR = "D:\\Cloud\\NBGI\\DARK SOULS REMASTERED"

def backup_saves(init):
    for path_dir in listdir(PATH_DSR):
        # find save folder
        path_dir_full = path.join(PATH_DSR, path_dir)
        print(path_dir_full)
        if not path.isfile(path_dir_full):
            for file in (x for x in listdir(path_dir_full) if path.isfile(path.join(path_dir_full, x))):
                # get name of the save
                name_save, name_extension = path.splitext(file)
                path_dir_backup = path.join(path_dir_full, f"{name_save}-BACKUP")
                path_save = path.join(path_dir_full, file)
                # get timestamps
                tSave = path.getmtime(path_save)
                tNow = time()
                # save backup
                if init or (tNow - tSave) < 600:
                    # create folder with save name if it doesn't exist yet
                    if not path.exists(path_dir_backup):
                        makedirs(path_dir_backup)
                    # create backup file
                    timeStamp = strftime("%Y_%H_%M_%S", localtime(tNow))
                    timePrint = strftime("%H:%M", localtime(tNow))
                    name_backup = f"{name_save}-BACKUP_{timeStamp}{name_extension}"
                    path_backup = path.join(path_dir_backup, name_backup)
                    copyfile(path_save, path_backup)
                    print(f"{timePrint}   saving backup of {name_save}:")
                    spacing = " " * len(timePrint)
                    print(f"{spacing}   -> {name_backup}")

def main():
    backup_saves(True)
    while True:
        backup_saves(False)
        iSleep = 60 * MINUTES_X
        print(f"\nsleeping for {MINUTES_X} minutes\n")
        sleep(iSleep)

if __name__ == '__main__':
    main()
