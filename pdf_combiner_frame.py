import tkinter as tk
from business import combiner
from guicomponents import DirectorySelectRow, ProgressBar, RowButton, TreeViewFrame
from guicomponents.config import *
from os import path
from tkinter import messagebox, ttk
from utils.helper_methods import prompt_to_open_folder

SELECT_SOURCE_FOLDER_MESSAGE = 'Select Source Folder'
SELECT_DESTINATION_FOLDER_MESSAGE = 'Select Output Folder'
SOURCE_IID = 'source'


class PdfCombinerFrame(tk.Frame):
    """
    Control the state of the directories we choose from.
    """

    def __init__(self, parent):
        """
        Initialize the GUI with the necessary components
        """
        self.parent = parent
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)

        # Source folder selection
        self.source_directory_var = tk.StringVar(self)
        self.source_select_row = DirectorySelectRow(self,
                                                    self.source_directory_var,
                                                    'Source Folder:',
                                                    SELECT_SOURCE_FOLDER_MESSAGE,
                                                    self.set_preview_tree)

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
        self.preview_frame = TreeViewFrame(self)

        # Destination folder selection
        self.destination_directory_var = tk.StringVar(self)
        self.destination_select_row = DirectorySelectRow(self,
                                                         self.destination_directory_var,
                                                         'Destination Folder:',
                                                         SELECT_DESTINATION_FOLDER_MESSAGE)
        self.progress_bar = ProgressBar(self,
                                        task_func=self.combine_pdfs_task,
                                        task_outcome_func_map=self.get_msg_task_map(),
                                        progress_title='Combining Pdfs',
                                        progress_text='Combining Pdfs...')

        # Combine pdfs button
        self.combinePdfsButton = RowButton(
            self,
            text='Combine PDFs',
            command=self.combine_button_listener
        )

    def combine_button_listener(self):
        """
            Validate we have the data we need to perform action and then go for it
        """
        if self.source_directory_var.get() is None or len(self.source_directory_var.get()) == 0:
            messagebox.showerror(SELECT_SOURCE_FOLDER_MESSAGE, "You must select a folder to read the pdfs from!")
        elif self.destination_directory_var.get() is None or len(self.destination_directory_var.get()) == 0:
            messagebox.showerror(SELECT_DESTINATION_FOLDER_MESSAGE, "You must select a folder to save the pdfs in!")
        else:
            try:
                self.toggle_button_disable(True)
                self.progress_bar.perform_action()
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "An unexpected error occurred, please try again.")

    def combine_pdfs_task(self, signal_queue, progress_var):
        """
            Perform the actual pdf merging
        """
        try:
            result_files = []
            directories_list = [self.source_directory_var.get()] + \
                combiner.get_child_dirs(self.source_directory_var.get())
            # combine pdfs in first layer of children
            for directory in directories_list:
                print("Combining files in: {}".format(directory))
                result_file = combiner.combine_docs_in_directory(directory,
                                                                 self.destination_directory_var.get(),
                                                                 include_jpg=self.include_jpg_var.get(),
                                                                 include_xps=self.include_xps_var.get(),
                                                                 progress_var=progress_var)
                if result_file:
                    result_files.append(result_file)

            # print results to stdout
            print("Finished combining all pdfs. Written files: ")
            for result_file in result_files:
                print("* {}".format(result_file))
            if len(result_files) > 0:
                signal_queue.put(TASK_FINISHED_MESSAGE)
            else:
                signal_queue.put(TASK_NOOP_MESSAGE)
        except Exception as e:
            print(e)
            signal_queue.put(TASK_ERROR_MESSAGE)
        finally:
            self.toggle_button_disable(False)

    def get_msg_task_map(self):
        return {
            TASK_FINISHED_MESSAGE: lambda: prompt_to_open_folder(self.destination_directory_var.get(),
                                                                 message_text="We have successfully "
                                                                              "merged the files. Open "
                                                                              "destination folder?"),
            TASK_ERROR_MESSAGE: lambda: messagebox.showerror("Error!",
                                                             "Encountered an error "
                                                             "when trying to combine pdfs."),
            TASK_NOOP_MESSAGE: lambda: messagebox.showerror("No Files Found!",
                                                            "No files were found to combine in your directory!")
        }

    def set_preview_tree(self):
        """
            Set the tree-view previewing which files to aggregate.
            I hate this method but I'm too lazy to clean it up.
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
                                text=path.split(self.source_directory_var.get())[1],
                                open=True)
            # display any pdfs in root
            root_pdfs = combiner.get_files_to_merge_in_dir(self.source_directory_var.get(),
                                                           include_jpg=self.include_jpg_var.get(),
                                                           include_xps=self.include_xps_var.get())
            for root_pdf in root_pdfs:
                preview_tree.insert(SOURCE_IID,
                                    'end',
                                    text=path.split(root_pdf)[1])
            file_count = len(root_pdfs)

            # get all its child directories
            children = combiner.get_child_dirs(self.source_directory_var.get())
            for child in children:
                preview_tree.insert(SOURCE_IID,
                                    'end',
                                    child,
                                    text=path.split(child)[1])
                # any of its pdfs there
                child_pdfs = combiner.get_files_to_merge_in_dir(child,
                                                                include_jpg=self.include_jpg_var.get(),
                                                                include_xps=self.include_xps_var.get())
                for child_pdf in child_pdfs:
                    preview_tree.insert(child,
                                        'end',
                                        text=path.split(child_pdf)[1])

                file_count = file_count + len(child_pdfs)
        self.progress_bar.progress_goal = file_count

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
