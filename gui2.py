import tkinter as tk
from file_mover_frame import FileMoverFrame
from tkinter import ttk
from utils import icon

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
        combiner_tab = ttk.Frame(tab_control)
        tab_control.add(FileMoverFrame(tab_control), text='File Mover')
        tab_control.add(combiner_tab, text='Pdf Combiner')
        tab_control.pack(expand=1, fill="both")

        ttk.Label(combiner_tab, text="Pdf Combiner").grid(column=0, row=0, padx=30, pady=30)

        # Step 2 - The Pdf Combiner Move
        # TODO Package components into a big gui frame
        # TODO pull out common components
        # TODO merge both of these into a common root gui

        # TODO: test test test!


window = tk.Tk()
window.wm_title(TITLE)
window.minsize(200, 10)
window.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))
root_gui = RootGui(parent=window)
root_gui.mainloop()
