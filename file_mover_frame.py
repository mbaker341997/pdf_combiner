import tkinter as tk
from business import directory_mover
from guicomponents import *
from os import path, scandir
from utils import helper_methods

SOURCE_IID = 'source'


class FileMoverFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # choose the input directory
        self.source_directory_var = tk.StringVar(self)
        DirectorySelectRow(self,
                           self.source_directory_var,
                           'Source Folder:',
                           'Select Source Folder',
                           self.set_preview_tree)

        # treeview showing the files to be moved
        self.tree_view_frame = TreeViewFrame(self)

        # move button
        self.fire_button = RowButton(self, text='Move Files', command=self.move_files)

        # TODO: Help button explaining what this is doing
        # TODO: loading bar
        # TODO: load test with something like 10,000 files

    def move_files(self):
        source_directory = self.source_directory_var.get()
        if source_directory:
            directory_mover.move_files(source_directory)
            helper_methods.open_folder(source_directory)

    def set_preview_tree(self):
        preview_tree = self.tree_view_frame.preview_tree
        preview_tree.delete(*preview_tree.get_children())
        source_dir = self.source_directory_var.get()
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
