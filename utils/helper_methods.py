import os
import platform
import subprocess


def open_folder(folder_name):
    if platform.system() == "Windows":
        os.startfile(folder_name)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", folder_name])
    else:
        subprocess.Popen(["xdg-open", folder_name])
