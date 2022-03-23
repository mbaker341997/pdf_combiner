import tkinter as tk
from file_mover_frame import FileMoverFrame
from guicomponents import config, help_popup, styles
from pdf_combiner_frame import PdfCombinerFrame
from tkinter import ttk
from utils import icon

TITLE = 'PDF Handler'


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
                                 command=help_popup.show_help_popup)
        help_button.pack(side=tk.RIGHT)

        # tab control
        tab_control = ttk.Notebook(self)
        tab_control.add(PdfCombinerFrame(tab_control), text='Pdf Combiner')
        tab_control.add(FileMoverFrame(tab_control), text='File Mover')
        tab_control.pack(expand=1, fill="both")

        # TODO: load test with a large number of files
        # TODO: record demo video
        # TODO: create executable for windows


window = tk.Tk()
window.wm_title(TITLE)
window.minsize(200, 10)
window.iconphoto(False, tk.PhotoImage(data=icon.get_pdf_icon()))
root_gui = RootGui(parent=window)
root_gui.mainloop()

