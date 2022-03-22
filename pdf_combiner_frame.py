import os.path
import queue
import threading
import tkinter as tk
from business import combiner
from guicomponents import config, DirectorySelectRow, RowButton, TreeViewFrame
from tkinter import messagebox, ttk
from utils import helper_methods, icon

SELECT_SOURCE_FOLDER_MESSAGE = 'Select Source Folder'
SELECT_DESTINATION_FOLDER_MESSAGE = 'Select Output Folder'
STATE_KEY = 'state'
VALUE_KEY = 'value'
SOURCE_IID = 'source'
TASK_FINISHED_MESSAGE = "Task Finished!"
TASK_ERRORED_MESSAGE = "Task Errored Out!"
NO_FILES_FOUND_MESSAGE = "No Files Found!"
PROGRESS_BAR_LENGTH = 300


class PdfCombinerFrame(tk.Frame):
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

        # Queue to signal when our async process is done
        self.signal_queue = queue.Queue()

        # Source folder selection
        self.source_directory_var = tk.StringVar(self)
        self.source_select_row = DirectorySelectRow(self,
                                                    self.source_directory_var,
                                                    'Source Folder:',
                                                    SELECT_SOURCE_FOLDER_MESSAGE,
                                                    self.set_preview_tree)

        # Optional checkboxes for jpegs and xps file conversion
        filetypes_frame = ttk.Frame(self)
        filetypes_frame.pack(fill=tk.X, padx=config.PAD_X_AMOUNT, pady=config.PAD_Y_AMOUNT)

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
        self.preview_frame = TreeViewFrame(self)

        # Destination folder selection
        self.destination_directory_var = tk.StringVar(self)
        self.destination_select_row = DirectorySelectRow(self,
                                                         self.destination_directory_var,
                                                         'Destination Folder:',
                                                         SELECT_DESTINATION_FOLDER_MESSAGE)

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
        self.progress_bar.pack(padx=config.PAD_X_AMOUNT, pady=config.PAD_Y_AMOUNT, fill=tk.X)
        self.progress_bar['maximum'] = PROGRESS_BAR_LENGTH
        self.progress_window.withdraw()

        # Combine pdfs button
        self.combinePdfsButton = RowButton(
            self,
            text='Combine PDFs',
            command=self.combine_the_pdfs
        )

    def combine_the_pdfs(self):
        """
            Perform the actual pdf merging
        """
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
                                                       "We have successfully merged the files. "
                                                       "Open destination folder?",
                                                       icon=messagebox.INFO)
                if open_destination:
                    # Open results folder
                    helper_methods.open_folder(self.destination_directory_var.get())
            elif msg == TASK_ERRORED_MESSAGE:
                messagebox.showerror("Error!", "Encountered an error when trying to combine pdfs.")
            elif msg == NO_FILES_FOUND_MESSAGE:
                messagebox.showerror("No Files Found!", "No files were found to combine in your directory!")
        except queue.Empty:
            self.parent.after(100, self.process_queue)

    def set_preview_tree(self):
        """
            Set the treeview previewing which files to aggregate
        """
        preview_tree = self.preview_frame.preview_tree
        # clear it out first
        preview_tree.delete(*preview_tree.get_children())
        file_count = 0  # total number of files we plan on combining, used to track progress
        if self.source_directory_var.get():
            # source directory we selected as the root
            preview_tree.insert('',
                                'end',
                                SOURCE_IID,
                                text=os.path.split(self.source_directory_var.get())[1],
                                open=True)
            # display any pdfs in root
            root_pdfs = combiner.get_files_to_merge_in_dir(self.source_directory_var.get(),
                                                           include_jpg=self.include_jpg_var.get(),
                                                           include_xps=self.include_xps_var.get())
            for root_pdf in root_pdfs:
                preview_tree.insert(SOURCE_IID,
                                    'end',
                                    text=os.path.split(root_pdf)[1])
            file_count = len(root_pdfs)

            # get all its child directories
            children = combiner.get_child_dirs(self.source_directory_var.get())
            for child in children:
                preview_tree.insert(SOURCE_IID,
                                    'end',
                                    child,
                                    text=os.path.split(child)[1])
                # any of its pdfs there
                child_pdfs = combiner.get_files_to_merge_in_dir(child,
                                                                include_jpg=self.include_jpg_var.get(),
                                                                include_xps=self.include_xps_var.get())
                for child_pdf in child_pdfs:
                    preview_tree.insert(child,
                                        'end',
                                        text=os.path.split(child_pdf)[1])

                file_count = file_count + len(child_pdfs)
        self.num_files = file_count

    # toggle whether the combine and select directory labels are disabled
    def toggle_button_disable(self, disabled):
        if disabled:
            print("buttons disabled")
            self.source_select_row.button[STATE_KEY] = tk.DISABLED
            self.destination_select_row.button[STATE_KEY] = tk.DISABLED
            self.combinePdfsButton[STATE_KEY] = tk.DISABLED
        else:
            print("buttons enabled")
            self.source_select_row.button[STATE_KEY] = tk.NORMAL
            self.destination_select_row.button[STATE_KEY] = tk.NORMAL
            self.combinePdfsButton[STATE_KEY] = tk.NORMAL


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
