import tkinter as tk
from tkinter import ttk
from utils import icon
from .config import PAD_X_AMOUNT, PAD_Y_AMOUNT
from .styles import HEADING_STYLE_KEY, HELP_STYLE_KEY, TITLE_STYLE_KEY

HELP_WIDTH = 800


class HelpFrame(tk.Frame):
    def __init__(self, parent, what_text='', how_text=''):
        super().__init__(parent)
        what_heading = ttk.Label(self, text='What is this?', style=HEADING_STYLE_KEY)
        what_heading.pack(side=tk.TOP, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT * 2, anchor=tk.NW)
        what_descr = ttk.Label(self,
                               text=what_text,
                               wraplength=HELP_WIDTH,
                               style=HELP_STYLE_KEY)
        what_descr.pack(padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT, anchor=tk.NW)
        how_heading = ttk.Label(self, text='How do I use it?', style=HEADING_STYLE_KEY)
        how_heading.pack(side=tk.TOP, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT, anchor=tk.NW)
        how_descr = ttk.Label(self,
                              text=how_text,
                              wraplength=HELP_WIDTH,
                              style=HELP_STYLE_KEY,
                              anchor=tk.NW)
        how_descr.pack(padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT, anchor=tk.NW)


def show_help_popup():
    title = 'Help!'

    # New top-level
    help_window = tk.Toplevel()
    help_window.wm_title(title)
    help_window.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))
    help_window.minsize(200, 10)

    # Title
    help_title_label = ttk.Label(help_window, text=title, style=TITLE_STYLE_KEY)
    help_title_label.pack(side=tk.TOP, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT * 3)

    # Tab setup for each help
    tab_control = ttk.Notebook(help_window)
    combiner_frame = HelpFrame(tab_control,
                               what_text="PDF Combiner combines all pdfs of a directory into one file. "
                                         "The title of that new file will be the directory_name.pdf",
                               how_text="Select a source folder to choose where to begin the pdf scan from and "
                                        "PDF Combiner will combine the pdfs directly in that source folder "
                                        "into one file, and then will merge the pdfs of each of its child directories "
                                        "into their own files.\nIt does not look more than one sub-directory deep. "
                                        "Children, no grandchildren.\nDestination folder will be where your combined "
                                        "files are stored. Both a source folder and destination folder must be chosen "
                                        "before combining pdfs. Non-pdf files found in a folder under scan will be "
                                        "skipped.")
    mover_frame = HelpFrame(tab_control,
                            what_text="File Mover takes all files with a 7-character prefix followed by a \".\", "
                                      "\"\\\", or \"-\" and moves all files with the same prefix into a new child "
                                      "directory named with that same prefix.\nFiles 1234567.01, 1234567.02 will be"
                                      "moved into a new folder titled\"1234567\", for instance.",
                            how_text="Select the directory that has the files you want to have moved. The files will "
                                     "display in the little tree view below. THen press the button and all the files"
                                     "will be moved into their new directories.")
    tab_control.add(combiner_frame, text='Pdf Combiner')
    tab_control.add(mover_frame, text='File Mover')
    tab_control.pack(expand=1, fill="both")

    # ok button to close
    ok_button = ttk.Button(help_window, text="OK", command=help_window.destroy)
    ok_button.pack(padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
