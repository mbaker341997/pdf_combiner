import tkinter as tk
from business import mover
from guicomponents import DirectorySelectRow, ProgressBar, RowButton, TreeViewFrame
from guicomponents.config import *
from utils.helper_methods import prompt_to_open_folder
from os import path, scandir
from tkinter import messagebox

SELECT_SOURCE_FOLDER_MESSAGE = 'Select Source Folder'
SOURCE_IID = 'source'


class FileMoverFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # choose the input directory
        self.source_directory_var = tk.StringVar(self)
        self.directory_select_row = DirectorySelectRow(self,
                                                       self.source_directory_var,
                                                       'Source Folder:',
                                                       SELECT_SOURCE_FOLDER_MESSAGE,
                                                       self.set_preview_tree)

        # tree-view showing the files to be moved
        self.tree_view_frame = TreeViewFrame(self)

        self.progress_bar = ProgressBar(self,
                                        task_func=self.move_files,
                                        task_outcome_func_map=self.get_msg_func_map(),
                                        progress_title="Moving Files",
                                        progress_text="Moving files...")

        # move button
        self.move_button = RowButton(self, text='Move Files', command=self.move_button_onclick)

        # TODO: load test with something like 10,000 files

    def move_button_onclick(self):
        # make sure we have a source directory
        if not self.source_directory_var.get():
            messagebox.showerror(SELECT_SOURCE_FOLDER_MESSAGE, "You must select a folder to find the files to move!")
            return False
        else:
            self.progress_bar.perform_action()

    # task to run asynchronously for ProgressBar
    def move_files(self, signal_queue, progress_var):
        try:
            # Disable the buttons so as not to cause issues
            self.directory_select_row.button[STATE_KEY] = tk.DISABLED
            self.move_button[STATE_KEY] = tk.DISABLED

            # move the files
            mover.move_files(self.source_directory_var.get(), progress_var)
            # signal completion
            signal_queue.put(TASK_FINISHED_MESSAGE)
        except Exception as e:
            print(e)
            signal_queue.put(TASK_ERROR_MESSAGE)
        finally:
            self.reset_buttons_and_tree()

    # map of task outcomes to functions. These execute *after* the progress bar has closed
    def get_msg_func_map(self):
        return {
            TASK_FINISHED_MESSAGE: lambda: prompt_to_open_folder(self.source_directory_var.get(),
                                                                 message_text="We have successfully moved the files. "
                                                                              "Open folder to view?"),
            TASK_ERROR_MESSAGE: lambda: messagebox.showerror("Error!",
                                                             "Encountered an error when trying to combine pdfs.")
        }

    def reset_buttons_and_tree(self):
        self.set_preview_tree()
        self.directory_select_row.button[STATE_KEY] = tk.NORMAL
        self.move_button[STATE_KEY] = tk.NORMAL

    def set_preview_tree(self):
        preview_tree = self.tree_view_frame.preview_tree
        preview_tree.delete(*preview_tree.get_children())
        source_dir = self.source_directory_var.get()
        num_files = 0
        if source_dir:
            # source directory we selected as the root
            preview_tree.insert('',
                                tk.END,
                                SOURCE_IID,
                                text=path.split(source_dir)[1],
                                open=True)
            # all root files or directories
            with scandir(source_dir) as it:
                for entry in it:
                    preview_tree.insert(SOURCE_IID, tk.END, text=entry.name)
                    num_files = num_files + 1
        self.progress_bar.progress_goal = num_files
