import os.path
import platform
import queue
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from business import combiner
from utils import icon

TITLE = 'PDF Combiner'
SELECT_MESSAGE = 'Select'
SELECT_SOURCE_FOLDER_MESSAGE = 'Select Source Folder'
SELECT_DESTINATION_FOLDER_MESSAGE = 'Select Output Folder'
TEXT_KEY = 'text'
STATE_KEY = 'state'
VALUE_KEY = 'value'
PAD_X_AMOUNT = 10
PAD_Y_AMOUNT = 5
ENTRY_WIDTH = 75
SOURCE_IID = 'source'
HELP_TITLE = "Help - PDF Combiner"
HELP_WIDTH = 800
TASK_FINISHED_MESSAGE = "Task Finished!"
TASK_ERRORED_MESSAGE = "Task Errored Out!"
NO_FILES_FOUND_MESSAGE = "No Files Found!"
PROGRESS_BAR_LENGTH = 300


class PdfCombiner(tk.Frame):
    """
    Control the state of the directories we choose from.
    """
    def __init__(self, parent):
        """
        Initialize the GUI with the necessary components
        """
        self.parent = parent
        super().__init__(self.parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.parent.wm_title(TITLE)
        self.parent.minsize(200, 10)
        self.parent.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))

        # Queue to signal when our async process is done
        self.signal_queue = queue.Queue()

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
        self.source_directory_var = tk.StringVar(self)
        source_frame = ttk.Frame(self)
        self.source_button = ttk.Button(
            source_frame,
            text=SELECT_MESSAGE,
            command=lambda: self.get_directory(self.source_directory_var, SELECT_SOURCE_FOLDER_MESSAGE))
        self.get_directory_selection_row(source_frame,
                                         self.source_button,
                                         self.source_directory_var,
                                         'Source Folder:')

        # Optional checkboxes for jpegs and xps file conversion
        filetypes_frame = ttk.Frame(self)
        filetypes_frame.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)

        filetypes_label = ttk.Label(filetypes_frame, text='Non-pdf filetypes to also merge: ')
        filetypes_label.pack(side=tk.LEFT)

        self.include_jpg_var = tk.BooleanVar(self)
        jpg_checkbox = ttk.Checkbutton(filetypes_frame, text="JPG", variable=self.include_jpg_var,
                                       command=self.set_preview_tree)
        jpg_checkbox.pack(side=tk.LEFT)

        self.include_xps_var = tk.BooleanVar(self)
        xps_checkbox = ttk.Checkbutton(filetypes_frame, text="XPS", variable=self.include_xps_var,
                                       command=self.set_preview_tree)
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
        self.destination_directory_var = tk.StringVar(self)
        destination_frame = ttk.Frame(self)
        self.destination_button = ttk.Button(
            destination_frame,
            text=SELECT_MESSAGE,
            command=lambda: self.get_directory(self.destination_directory_var, SELECT_DESTINATION_FOLDER_MESSAGE))
        self.get_directory_selection_row(destination_frame,
                                         self.destination_button,
                                         self.destination_directory_var,
                                         'Destination Folder:')

        # Value to track the progress 
        self.progress_var = tk.IntVar(self)
        self.num_files = 0

        # Track progress
        self.progress_window = tk.Toplevel()
        self.progress_window.wm_title('Combining Pdfs')
        self.progress_window.iconphoto(self.progress_window, tk.PhotoImage(data=icon.get_pdf_icon()))
        self.progress_label = ttk.Label(self.progress_window, text='Combining Pdfs...')
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(self.progress_window, orient=tk.HORIZONTAL, length=PROGRESS_BAR_LENGTH,
                                            mode='determinate')
        self.progress_bar.pack(padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT, fill=tk.X)
        self.progress_bar['maximum'] = PROGRESS_BAR_LENGTH
        self.progress_window.withdraw()

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
    def get_directory_selection_row(self,
                                    selection_frame,
                                    directory_button,
                                    directory_var,
                                    directory_label_text):
        directory_label = ttk.Label(selection_frame,
                                    text=directory_label_text)
        directory_entry = tk.Entry(selection_frame,
                                   width=ENTRY_WIDTH,
                                   textvariable=directory_var,
                                   state=tk.DISABLED,
                                   disabledbackground='white',
                                   disabledforeground='black')
        selection_frame.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        directory_label.pack(side=tk.LEFT)
        directory_entry.pack(side=tk.LEFT, padx=PAD_X_AMOUNT, fill=tk.X, expand=True)
        directory_button.pack(side=tk.RIGHT)

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
            try:
                directories_list = [self.source_directory_var.get()] + combiner.get_child_dirs(
                    self.source_directory_var.get())
                self.toggle_button_disable(True)
                CombinerTask(self.signal_queue,
                             directories_list,
                             self.destination_directory_var.get(),
                             self.include_jpg_var.get(),
                             self.include_xps_var.get(),
                             self.progress_var).start()
                self.progress_window.deiconify()
                self.parent.after(100, self.process_queue)
            except:
                messagebox.showerror("Error", "An unexpected error occurred, please try again.")

    def process_queue(self):
        if self.num_files > 0:
            self.progress_bar[VALUE_KEY] = (self.progress_var.get() / self.num_files) * PROGRESS_BAR_LENGTH
            self.progress_window.update()
        try:
            msg = self.signal_queue.get(0)
            print(msg)
            # clear progress value and reenable buttons
            self.progress_var.set(0)
            self.progress_bar[VALUE_KEY] = 0
            self.progress_window.withdraw()
            self.toggle_button_disable(False)
            if msg == TASK_FINISHED_MESSAGE:
                # End Task
                open_destination = messagebox.askyesno("Success!",
                                                       "We have successfully merged the files. Open destination folder?",
                                                       icon=messagebox.INFO)
                if open_destination:
                    # Open results folder
                    if platform.system() == "Windows":
                        os.startfile(self.destination_directory_var.get())
                    elif platform.system() == "Darwin":
                        subprocess.Popen(["open", self.destination_directory_var.get()])
                    else:
                        subprocess.Popen(["xdg-open", self.destination_directory_var.get()])
            elif msg == TASK_ERRORED_MESSAGE:
                messagebox.showerror("Error!", "Encountered an error when trying to combine pdfs.")
            elif msg == NO_FILES_FOUND_MESSAGE:
                messagebox.showerror("No Files Found!", "No files were found to combine in your directory!")
        except queue.Empty:
            self.parent.after(100, self.process_queue)

    """
    Set the treeview previewing which files to aggregate
    """
    def set_preview_tree(self):
        # clear it out first
        self.preview_tree.delete(*self.preview_tree.get_children())
        file_count = 0  # total number of files we plan on combining, used to track progress
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
            file_count = len(root_pdfs)

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

                file_count = file_count + len(child_pdfs)
        self.num_files = file_count

    # toggle whether the combine and select directory labels are disabled
    def toggle_button_disable(self, disabled):
        if disabled:
            print("buttons disabled")
            self.source_button[STATE_KEY] = tk.DISABLED
            self.destination_button[STATE_KEY] = tk.DISABLED
            self.combinePdfsButton[STATE_KEY] = tk.DISABLED
        else:
            print("buttons enabled")
            self.source_button[STATE_KEY] = tk.NORMAL
            self.destination_button[STATE_KEY] = tk.NORMAL
            self.combinePdfsButton[STATE_KEY] = tk.NORMAL

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
        help_title_label.pack(side=tk.TOP, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT * 3)

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


class CombinerTask(threading.Thread):
    def __init__(self, signal_queue, source_directories, destination, include_jpg, include_xps, progress_var):
        threading.Thread.__init__(self)
        self.signal_queue = signal_queue
        self.directories = source_directories
        self.destination = destination
        self.include_jpg = include_jpg
        self.include_xps = include_xps
        self.progress_var = progress_var

    def run(self):
        try:
            result_files = []
            # combine pdfs in first layer of children
            for directory in self.directories:
                print("Combining files in: {}".format(directory))
                result_file = combiner.combine_docs_in_directory(directory, self.destination, self.include_jpg,
                                                                 self.include_xps, self.progress_var)
                if result_file:
                    result_files.append(result_file)

            # print results to stdout
            print("Finished combining all pdfs. Written files: ")
            for result_file in result_files:
                print("* {}".format(result_file))
            if len(result_files) > 0:
                self.signal_queue.put(TASK_FINISHED_MESSAGE)
            else:
                self.signal_queue.put(NO_FILES_FOUND_MESSAGE)
        except Exception as e:
            print(e)
            self.signal_queue.put(TASK_ERRORED_MESSAGE)


window = tk.Tk()
pdf_combiner_gui = PdfCombiner(parent=window)
pdf_combiner_gui.mainloop()
