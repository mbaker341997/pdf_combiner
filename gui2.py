import tkinter as tk
from tkinter import ttk
from pdfcombiner import icon
from guicomponents import DirectorySelectRow

# TODO: Cram this into a constants file
TITLE = 'PDF Combiner'
PAD_X_AMOUNT = 10
PAD_Y_AMOUNT = 5


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
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Tab 1')
        tab_control.add(tab2, text='Tab 2')
        tab_control.pack(expand=1, fill="both")

        ttk.Label(tab1, text="Directory Mover").grid(column=0, row=0, padx=30, pady=30)
        ttk.Label(tab2, text="Pdf Combiner").grid(column=0, row=0, padx=30, pady=30)

        # Step 1 - The Directory Combiner
        # Let it choose the input directory
        self.source_directory_var = tk.StringVar(self)
        DirectorySelectRow(self, self.source_directory_var, 'Source Folder:', 'Select Source Folder', self.dummy)
        # TODO: Treeview showing the files to be combined
        # TODO: Fire button
        # TODO: Help button explaining what this is doing

        # Step 2 - The Pdf Combiner Move
        # TODO Package components into a big gui frame
        # TODO pull out common components
        # TODO merge both of these into a common root gui

        # TODO: test test test!

    def dummy(self):
        print(self.source_directory_var.get())
        print("oh wow it works!")


window = tk.Tk()
window.wm_title(TITLE)
window.minsize(200, 10)
window.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))
root_gui = RootGui(parent=window)
root_gui.mainloop()
