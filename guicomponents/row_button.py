from tkinter import BOTH, ttk
from .config import PAD_X_AMOUNT, PAD_Y_AMOUNT


# Big button that takes up an entire row
class RowButton(ttk.Button):
    def __init__(self, parent, text='Go', command=None):
        super().__init__(parent, text=text, command=command)
        self.pack(fill=BOTH, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
