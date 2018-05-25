from os import path, listdir, makedirs, remove
from shutil import copyfile
from time import time, localtime, strftime, sleep
from datetime import datetime
import sys

"""
automatic DSR backup file creation
(1) creates backups upon start
(2) creates backups every saveInterval minutes defined below. Default: 5
(3) deletes backups if there are greater than maxBackups in backup directory. Default: 15
note: the documents folder has to be set as FOLDER_documents below. Default: 'documents'
note: auto save only for files which have been modified in the last 10 minutes
note: should be compiled using PyInstaller
"""

# insert the name of the windows documents folder
# depends either on locale (by default) or user setting
DOCUMENTS_NAME = "documents"
# Defaults
DEFAULT_DSR_PATH = path.join(path.expandvars("%userprofile%"), DOCUMENTS_NAME, "NBGI", "DARK SOULS REMASTERED")
DEFAULT_SAVE_INTERVAL = 5
DEFAULT_MAX_BACKUPS = 15

def backup_saves(init, savePath, maxBackups):
    for path_dir in listdir(savePath):
        # find save folder
        path_dir_full = path.join(savePath, path_dir)
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
                    # delete oldest backup if more than maxBackups exists
                    while len(listdir(path_dir_backup)) > maxBackups:
                        oldestBackupPath = ""
                        oldestBackupTime = sys.maxsize
                        for backup in listdir(path_dir_backup):
                            currentBackupPath = path.join(path_dir_backup, backup)
                            currentBackupTime = path.getmtime(currentBackupPath)
                            if currentBackupTime < oldestBackupTime:
                                oldestBackupPath = currentBackupPath
                                oldestBackupTime = currentBackupTime
                        remove(oldestBackupPath)
                        removedBackupFile = path.basename(oldestBackupPath)
                        print(f"{spacing}   removed backup of {name_save}:")
                        print(f"{spacing}   -> {removedBackupFile}")

def main():
    dsrPath = DEFAULT_DSR_PATH
    saveInterval = DEFAULT_SAVE_INTERVAL
    maxBackups = DEFAULT_MAX_BACKUPS
    # Optional command line arguments
    # Usage: <DSR Path> <Save Interval (Minutes)> <Maximum Backups to Keep>
    if len(sys.argv) == 4:
        dsrPath = sys.argv[1]
        saveInterval = int(sys.argv[2])
        maxBackups = int(sys.argv[3])

    # Check if save directory exists. Exit otherwise
    if not path.exists(dsrPath):
        print(f"Dark Souls Remastered save directory not found at {dsrPath}")
        sys.exit()

    backup_saves(True, dsrPath, maxBackups)
    iSleep = 60 * saveInterval
    while True:
        backup_saves(False, dsrPath, maxBackups)
        print(f"\nsleeping for {saveInterval} minutes\n")
        sleep(iSleep)

if __name__ == '__main__':
    main()
