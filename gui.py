import os.path
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdfcombiner import combiner, icon

TITLE = 'PDF Combiner'
SELECT_MESSAGE = 'Select'
SELECT_SOURCE_FOLDER_MESSAGE = 'Select Source Folder'
SELECT_DESTINATION_FOLDER_MESSAGE = 'Select Output Folder'
TEXT_KEY = 'text'
STATE_KEY = 'state'
PAD_X_AMOUNT = 10
PAD_Y_AMOUNT = 5
ENTRY_WIDTH = 75
SOURCE_IID = 'source'
HELP_TITLE = "Help - PDF Combiner"
HELP_WIDTH = 800


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
        parent.wm_title(TITLE)
        parent.minsize(200, 10)
        parent.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))

        # styling
        style = ttk.Style()
        self.title_style_key = "CombinerTitle.TLabel"
        style.configure(self.title_style_key, font='helvetica 24')
        self.heading_style_key = "CombinerHeading.TLabel"
        style.configure(self.heading_style_key, font='helvetica 20')
        self.help_style_key = "HelpBody.TLabel"
        style.configure(self.help_style_key, font='helvetica 16')

        # Top Area - title and help button
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT * 3)
        # title labeling
        self.title_label = ttk.Label(top_frame, text=TITLE, style=self.title_style_key)
        self.title_label.pack(side=tk.LEFT)
        help_button = ttk.Button(top_frame,
                                      text="Help!",
                                      command=self.help_popup)
        help_button.pack(side=tk.RIGHT)
        separator = ttk.Separator(self)
        separator.pack(fill=tk.X, padx=PAD_X_AMOUNT)

        # Source folder selection
        self.source_directory_var = tk.StringVar()
        self.get_directory_selection_row(self.source_directory_var, 'Source Folder:', SELECT_SOURCE_FOLDER_MESSAGE)

        # Optional checkboxes for jpegs and xps file conversion
        filetypes_frame = ttk.Frame(self)
        filetypes_frame.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)

        filetypes_label = ttk.Label(filetypes_frame, text='Non-pdf filetypes to also merge: ')
        filetypes_label.pack(side=tk.LEFT)

        self.include_jpg_var = tk.BooleanVar()
        jpg_checkbox = ttk.Checkbutton(filetypes_frame, text="JPG", variable=self.include_jpg_var, command=self.set_preview_tree)
        jpg_checkbox.pack(side=tk.LEFT)
        
        self.include_xps_var = tk.BooleanVar()
        xps_checkbox = ttk.Checkbutton(filetypes_frame, text="XPS", variable=self.include_xps_var, command=self.set_preview_tree)
        xps_checkbox.pack(side=tk.LEFT)


        # Get child directories and display
        preview_frame = ttk.Frame(self)
        preview_frame.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        self.preview_tree = ttk.Treeview(preview_frame, show='tree')
        y_bar = tk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.configure(yscroll=y_bar.set)
        y_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_tree.pack(fill=tk.X)

        # Destination folder selection
        self.destination_directory_var = tk.StringVar()
        self.get_directory_selection_row(self.destination_directory_var,
                                         'Destination Folder:',
                                         SELECT_DESTINATION_FOLDER_MESSAGE)
        # Combine pdfs button
        self.combinePdfsButton = ttk.Button(
            self,
            text='Combine PDFs',
            command=self.combine_the_pdfs
        )
        self.combinePdfsButton.pack(fill=tk.BOTH, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)

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
        directory_entry.pack(side=tk.LEFT, padx=PAD_X_AMOUNT, fill=tk.X, expand=True)
        select_button.pack(side=tk.RIGHT)

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
        if self.source_directory_var.get() is None or len(self.source_directory_var.get()) == 0:
            messagebox.showerror(SELECT_SOURCE_FOLDER_MESSAGE, "You must select a folder to read the pdfs from!")
        elif self.destination_directory_var.get() is None or len(self.destination_directory_var.get()) == 0:
            messagebox.showerror(SELECT_DESTINATION_FOLDER_MESSAGE, "You must select a folder to save the pdfs in!")
        else:
            self.title_label[TEXT_KEY] = "Combining pdfs..."
            self.combinePdfsButton[STATE_KEY] = tk.DISABLED
            try:
                result_files = combiner.combine_all_docs(self.source_directory_var.get(),
                                                         self.destination_directory_var.get(),
                                                         include_jpg=self.include_jpg_var.get(), 
                                                         include_xps=self.include_xps_var.get())
                if len(result_files) > 0:
                    open_destination = messagebox.askyesno("Success!",
                                                           "We have successfully written combined pdf files to: {}\n"
                                                           "Open destination folder?".
                                                           format(self.destination_directory_var.get()),
                                                           icon=messagebox.INFO)
                    if open_destination:
                        # Open results folder
                        if platform.system() == "Windows":
                            os.startfile(self.destination_directory_var.get())
                        elif platform.system() == "Darwin":
                            subprocess.Popen(["open", self.destination_directory_var.get()])
                        else:
                            subprocess.Popen(["xdg-open", self.destination_directory_var.get()])
                else:
                    messagebox.showwarning("No pdfs found!", "We were not able to find any pdfs to combine in {}"
                                           .format(self.source_directory_var.get()))
            except:
                messagebox.showerror("Error", "An unexpected error occurred, please try again.")

            self.title_label[TEXT_KEY] = TITLE
            self.combinePdfsButton[STATE_KEY] = tk.NORMAL

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
                                     text=os.path.split(self.source_directory_var.get())[1],
                                     open=True)
            # display any pdfs in root
            root_pdfs = combiner.get_files_to_merge_in_dir(self.source_directory_var.get(), 
                                                           include_jpg=self.include_jpg_var.get(), 
                                                           include_xps=self.include_xps_var.get())
            for root_pdf in root_pdfs:
                self.preview_tree.insert(SOURCE_IID,
                                         'end',
                                         text=os.path.split(root_pdf)[1])

            # get all its child directories
            children = combiner.get_child_dirs(self.source_directory_var.get())
            for child in children:
                self.preview_tree.insert(SOURCE_IID,
                                         'end',
                                         child,
                                         text=os.path.split(child)[1])
                # any of its pdfs there
                child_pdfs = combiner.get_files_to_merge_in_dir(child, 
                                                                include_jpg=self.include_jpg_var.get(), 
                                                                include_xps=self.include_xps_var.get())
                for child_pdf in child_pdfs:
                    self.preview_tree.insert(child,
                                             'end',
                                             text=os.path.split(child_pdf)[1])

    """
    Create a popup message to display help information
    """
    def help_popup(self):
        # New top-level
        help_window = tk.Toplevel()
        help_window.wm_title(HELP_TITLE)
        help_window.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))

        # Title
        help_title_label = ttk.Label(help_window, text=HELP_TITLE, style=self.title_style_key)
        help_title_label.pack(side=tk.TOP, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT*3)

        # Actual Help Messages
        what_heading = ttk.Label(help_window, text='What is this?', style=self.heading_style_key)
        what_heading.pack(side=tk.TOP, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        what_descr = ttk.Label(help_window,
                               text="PDF Combiner combines all pdfs of a directory into one file. "
                                    "The title of that new file will be the directory_name.pdf",
                               wraplength=HELP_WIDTH,
                               style=self.help_style_key)
        what_descr.pack(padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        how_heading = ttk.Label(help_window, text='How do I use it?', style=self.heading_style_key)
        how_heading.pack(side=tk.TOP, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        how_descr = ttk.Label(help_window,
                              text="Select a source folder to choose where to begin the pdf scan from and "
                                   "PDF Combiner will combine the pdfs directly in that source folder "
                                   "into one file, and then will merge the pdfs of each of its child directories "
                                   "into their own files. It does not look more than one sub-directory deep. "
                                   "Children, no grandchildren. Destination folder will be where your combined files "
                                   "are stored. Both a source folder and destination folder must be chosen before "
                                   "combining pdfs. Non-pdf files found in a folder under scan will be skipped.",
                              wraplength=HELP_WIDTH,
                              style=self.help_style_key)
        how_descr.pack(padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        ok_button = ttk.Button(help_window, text="OK", command=help_window.destroy)
        ok_button.pack(padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        help_window.mainloop()


window = tk.Tk()
pdf_combiner_gui = PdfCombiner(parent=window)
pdf_combiner_gui.mainloop()
