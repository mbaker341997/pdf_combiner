import tkinter as tk
from tkinter import ttk
from .config import PAD_X_AMOUNT, PAD_Y_AMOUNT


class TreeViewFrame(tk.Frame):
    def __init__(self, parent):
        # initialize
        super().__init__(parent)
        self.pack(fill=tk.BOTH, padx=PAD_X_AMOUNT, pady=PAD_Y_AMOUNT)
        self.preview_tree = ttk.Treeview(self, show='tree')
        y_bar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.preview_tree.yview)
        self.preview_tree.configure(yscroll=y_bar.set)
        y_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_tree.pack(fill=tk.BOTH)
