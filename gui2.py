import tkinter as tk
from tkinter import ttk
from os import path, scandir
from pdfcombiner import icon
from guicomponents import DirectorySelectRow, TreeViewFrame

# TODO: Cram this into a constants file
TITLE = 'PDF Handler'
PAD_X_AMOUNT = 10
PAD_Y_AMOUNT = 5

SOURCE_IID = 'source'


class RootGui(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)

        # TODO: init styling in its own method, put the keys and configs into a big map or something
        # styling
        style = ttk.Style()
        self.title_style_key = "CombinerTitle.TLabel"
        style.configure(self.title_style_key, font='helvetica 24')
        self.heading_style_key = "CombinerHeading.TLabel"
        style.configure(self.heading_style_key, font='helvetica 20')
        self.help_style_key = "HelpBody.TLabel"
        style.configure(self.help_style_key, font='helvetica 16')

        # TODO: its own lil class?
        # Top area - title
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT * 3)
        # title labeling
        self.title_label = ttk.Label(top_frame, text=TITLE, style=self.title_style_key)
        self.title_label.pack(side=tk.LEFT)

        # tab control
        tab_control = ttk.Notebook(self)
        mover_tab = ttk.Frame(tab_control)
        combiner_tab = ttk.Frame(tab_control)
        tab_control.add(mover_tab, text='File Mover')
        tab_control.add(combiner_tab, text='Pdf Combiner')
        tab_control.pack(expand=1, fill="both")

        ttk.Label(combiner_tab, text="Pdf Combiner").grid(column=0, row=0, padx=30, pady=30)

        # Step 1 - The Directory Combiner
        # Let it choose the input directory
        self.source_directory_var = tk.StringVar(self)
        DirectorySelectRow(mover_tab,
                           self.source_directory_var,
                           'Source Folder:',
                           'Select Source Folder',
                           self.set_preview_tree)

        # TODO: Treeview showing the files to be moved
        self.tree_view_frame = TreeViewFrame(mover_tab)
        # TODO: Fire button
        # TODO: Help button explaining what this is doing

        # Step 2 - The Pdf Combiner Move
        # TODO Package components into a big gui frame
        # TODO pull out common components
        # TODO merge both of these into a common root gui

        # TODO: test test test!

    def set_preview_tree(self):
        # TODO: make this fill the treeview
        print(self.source_directory_var.get())
        print("oh wow it works!")
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


window = tk.Tk()
window.wm_title(TITLE)
window.minsize(200, 10)
window.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))
root_gui = RootGui(parent=window)
root_gui.mainloop()
