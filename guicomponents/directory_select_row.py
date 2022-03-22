import tkinter as tk
from .config import PAD_X_AMOUNT, PAD_Y_AMOUNT
from tkinter import filedialog, ttk

ENTRY_WIDTH = 75
SELECT_MESSAGE = 'Select'


class DirectorySelectRow(tk.Frame):
    def __init__(self, parent, directory_var, label_text, select_message, on_select_func=lambda *a, **k: None):
        # initialize
        super().__init__(parent)
        self.directory_var = directory_var
        self.label_text = label_text
        self.select_message = select_message
        self.on_select_func = on_select_func

        # label for row
        label = ttk.Label(self, text=label_text)

        # entry area
        entry = tk.Entry(self,
                         width=ENTRY_WIDTH,
                         textvariable=directory_var,
                         state=tk.DISABLED,
                         disabledbackground='white',
                         disabledforeground='black')

        # button
        button = ttk.Button(
            self,
            text='Select',
            command=lambda: self.get_directory())

        # pack everything
        self.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.LEFT, padx=PAD_X_AMOUNT, fill=tk.X, expand=True)
        button.pack(side=tk.RIGHT)

    """
    Get a directory and set the appropriate StringVar.
    """
    def get_directory(self):
        directory = filedialog.askdirectory(title=self.select_message, mustexist=True)
        if directory:
            self.directory_var.set(directory)
            self.on_select_func()
