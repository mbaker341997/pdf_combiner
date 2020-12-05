import pdfcombiner
import tkinter as tk
from os import path
from tkinter import filedialog, messagebox, ttk

TITLE = 'PDF Combiner'
SELECT_MESSAGE = 'Select'
SELECT_SOURCE_FOLDER_MESSAGE = 'Select Source Folder'
SELECT_DESTINATION_FOLDER_MESSAGE = 'Select Output Folder'
WINDOW_WIDTH = 50
COMPONENT_HEIGHT = 5
TEXT_KEY = 'text'
PAD_X_AMOUNT = 10
PAD_Y_AMOUNT = 5
ENTRY_WIDTH = 75
SOURCE_IID = 'source'


class PdfCombiner(tk.Frame):
    """
    Control the state of the directories we choose from.
    """
    def __init__(self, parent):
        """
        Initialize the GUI with the necessary components
        """
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)

        # set parent's title
        parent.title(TITLE)

        # TODO: file icon
        # TODO: set minimum width/height

        # Top Area - title and help button
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        # title labeling
        self.title_label = ttk.Label(self.top_frame, text=TITLE)
        self.title_label.pack(side=tk.LEFT)
        # TODO: help dialog
        self.help_button = ttk.Button(self.top_frame, text="Help!")
        self.help_button.pack(side=tk.RIGHT)
        self.separator = ttk.Separator(self)
        self.separator.pack(fill=tk.X, padx=PAD_X_AMOUNT)

        # Source folder selection
        self.source_directory_var = tk.StringVar()
        self.get_directory_selection_row(self.source_directory_var, 'Source Folder:', SELECT_SOURCE_FOLDER_MESSAGE)

        # Get child directories and display
        self.preview_frame = ttk.Frame(self)
        self.preview_frame.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        self.preview_tree = ttk.Treeview(self.preview_frame, show='tree')
        y_bar = tk.Scrollbar(self.preview_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.configure(yscroll=y_bar.set)
        y_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_tree.pack(fill=tk.X)

        # Destination folder selection
        self.destination_directory_var = tk.StringVar()
        self.get_directory_selection_row(self.destination_directory_var,
                                         'Destination Folder:',
                                         SELECT_DESTINATION_FOLDER_MESSAGE)
        # Get destination folder with pdfs

        self.combinePdfsButton = ttk.Button(
            self,
            text='Combine PDFs',
            command=self.combine_the_pdfs
        )
        self.combinePdfsButton.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        # TODO: open results folder

    """
    Build a directory selection row.
    """
    def get_directory_selection_row(self, directory_var, directory_label_text, dialog_message):
        selection_frame = ttk.Frame(self)
        directory_label = ttk.Label(selection_frame,
                                    text=directory_label_text)
        directory_entry = tk.Entry(selection_frame,
                                   width=ENTRY_WIDTH,
                                   textvariable=directory_var,
                                   state=tk.DISABLED,
                                   disabledbackground='white',
                                   disabledforeground='black')
        select_button = ttk.Button(
            selection_frame,
            text=SELECT_MESSAGE,
            command=lambda: self.get_directory(directory_var, dialog_message))
        selection_frame.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        directory_label.pack(side=tk.LEFT)
        select_button.pack(side=tk.RIGHT)
        directory_entry.pack(side=tk.RIGHT, padx=PAD_X_AMOUNT)

    """
    Get a directory and set the appropriate StringVar.
    """
    def get_directory(self, string_var, select_message):
        directory = filedialog.askdirectory(title=select_message, mustexist=True)
        if directory:
            string_var.set(directory)
            if string_var is self.source_directory_var:
                self.set_preview_tree()

    """
    Perform the actual pdf merging
    """
    def combine_the_pdfs(self):
        if self.source_directory_var.get() is None:
            messagebox.showerror(SELECT_SOURCE_FOLDER_MESSAGE, "You must select a folder to read the pdfs from!")
        elif self.destination_directory_var.get() is None:
            messagebox.showerror(SELECT_DESTINATION_FOLDER_MESSAGE, "You must select a folder to save the pdfs in!")
        else:
            result_files = pdfcombiner.combine_all_pdfs(self.source_directory_var.get(),
                                                        self.destination_directory_var.get())
            if len(result_files) > 0:
                messagebox.showinfo("Success!", "We have successfully written combined pdf files to: {}".
                                    format(self.destination_directory_var.get()))
            else:
                messagebox.showwarning("No pdfs found!", "We were not able to find any pdfs to combine in {}"
                                       .format(self.source_directory_var.get()))

    """
    Set the treeview previewing which files to aggregate
    """
    def set_preview_tree(self):
        # clear it out first
        self.preview_tree.delete(*self.preview_tree.get_children())
        if self.source_directory_var.get():
            # source directory we selected as the root
            self.preview_tree.insert('',
                                     'end',
                                     SOURCE_IID,
                                     text=path.split(self.source_directory_var.get())[1],
                                     open=True)
            # display any pdfs in root
            root_pdfs = pdfcombiner.get_pdfs_in_dir(self.source_directory_var.get())
            for root_pdf in root_pdfs:
                self.preview_tree.insert(SOURCE_IID,
                                         'end',
                                         text=path.split(root_pdf)[1])

            # get all its child directories
            children = pdfcombiner.get_child_dirs(self.source_directory_var.get())
            for child in children:
                self.preview_tree.insert(SOURCE_IID,
                                         'end',
                                         child,
                                         text=path.split(child)[1])
                # any of its pdfs there
                child_pdfs = pdfcombiner.get_pdfs_in_dir(child)
                for child_pdf in child_pdfs:
                    self.preview_tree.insert(child,
                                             'end',
                                             text=path.split(child_pdf)[1])


window = tk.Tk()
pdf_combiner_gui = PdfCombiner(parent=window)
pdf_combiner_gui.mainloop()
