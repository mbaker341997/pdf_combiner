import tkinter as tk
from file_mover_frame import FileMoverFrame
from guicomponents import config, styles
from pdf_combiner_frame import PdfCombinerFrame
from tkinter import ttk
from utils import icon
import webbrowser

TITLE = 'PDF Handler'
ANCHOR_MAP = {
    0: 'pdf-combiner',
    1: 'file-mover'
}


class RootGui(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)

        # styling
        styles.init_styles()

        # Top area - title
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=config.PAD_X_AMOUNT, pady=config.PAD_Y_AMOUNT * 3)
        # title labeling
        self.title_label = ttk.Label(top_frame, text=TITLE, style=styles.TITLE_STYLE_KEY)
        self.title_label.pack(side=tk.LEFT)
        help_button = ttk.Button(top_frame,
                                 text="Help!",
                                 command=self.open_help)
        help_button.pack(side=tk.RIGHT)

        # tab control
        self.tab_control = ttk.Notebook(self)
        self.tab_control.add(PdfCombinerFrame(self.tab_control), text='Pdf Combiner')
        self.tab_control.add(FileMoverFrame(self.tab_control), text='File Mover')
        self.tab_control.pack(expand=1, fill="both")

        # TODO: create executable for windows
        # TODO: record demo video

    def open_help(self):
        anchor = ANCHOR_MAP.get(self.tab_control.index(tk.CURRENT), 'pdf-handler')
        webbrowser.open(f'https://github.com/mbaker341997/pdf_combiner/blob/mainline/README.md#{anchor}')


window = tk.Tk()
window.wm_title(TITLE)
window.minsize(200, 10)
window.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))
root_gui = RootGui(parent=window)
root_gui.mainloop()

