from os import path, walk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

preview_filenames = []


def callback():
    preview_filenames.clear()
    directory_name = filedialog.askdirectory(title="Select base directory", mustexist=True)
    for (root, _, filenames) in walk(directory_name):
        for filename in filenames:
            preview_filenames.append(path.join(root, filename))
    print(directory_name)


# folder selection
window = tk.Tk()
window.Button(text="Select root directory", command=callback).pack(fill=tk.X)
tree = ttk.Treeview(window, columns="Filename")
window.mainloop()

# preview(?)

# button to activate

# output view
