import os
import platform
import subprocess
from tkinter import messagebox


def open_folder(folder_name):
    if platform.system() == "Windows":
        os.startfile(folder_name)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", folder_name])
    else:
        subprocess.Popen(["xdg-open", folder_name])


def prompt_to_open_folder(folder_name, message_text=None, message_title="Success!"):
    # Mention folder name in default message text
    if not message_text:
        message_text = f"Open folder: {folder_name}?"
    # prompt yes/no
    open_destination = messagebox.askyesno(message_title,
                                           message_text,
                                           icon=messagebox.INFO)
    if open_destination:
        # Open results folder
        open_folder(folder_name)
