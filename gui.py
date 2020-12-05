import pdfcombiner
import tkinter as tk
from tkinter import filedialog, messagebox

TITLE = 'PDF Combiner'
SOURCE_DIRECTORY_FORMAT = 'Source Folder: {}'
DESTINATION_DIRECTORY_FORMAT = 'Destination Folder: {}'
SELECT_SOURCE_FOLDER_MESSAGE = 'Select Source Folder'
SELECT_DESTINATION_FOLDER_MESSAGE = 'Select Output Folder'
WINDOW_WIDTH = 50
COMPONENT_HEIGHT = 5
TEXT_KEY = "text"


class PdfCombiner:
    """
    Control the state of the directories we choose from.
    """
    def __init__(self, parent):
        """
        Initialize the GUI with the necessary components
        """
        self.parent = parent
        self.parent.title(TITLE)

        self.source_directory = None
        self.destination_directory = None

        # title labeling
        self.title_label = tk.Label(text=TITLE, height=COMPONENT_HEIGHT, width=WINDOW_WIDTH)
        self.title_label.pack()

        # Source directory selection
        self.source_directory_label = tk.Label(text=SOURCE_DIRECTORY_FORMAT.format(self.source_directory),
                                               height=COMPONENT_HEIGHT)
        self.selectBaseButton = tk.Button(
            text=SELECT_SOURCE_FOLDER_MESSAGE,
            height=COMPONENT_HEIGHT,
            command=self.get_source_directory
        )
        self.selectBaseButton.pack()
        self.source_directory_label.pack()

        # TODO: display a preview of the child directories and files

        # Destination folder selection
        self.destination_directory_label = tk.Label(text=DESTINATION_DIRECTORY_FORMAT.format(self.destination_directory),
                                                    height=COMPONENT_HEIGHT)
        self.selectDestinationButton = tk.Button(
            text=SELECT_DESTINATION_FOLDER_MESSAGE,
            height=COMPONENT_HEIGHT,
            command=self.get_destination_directory
        )
        self.selectDestinationButton.pack()
        self.destination_directory_label.pack()

        self.combinePdfsButton = tk.Button(
            text='Combine PDFS',
            height=COMPONENT_HEIGHT,
            command=self.combine_the_pdfs
        )
        self.combinePdfsButton.pack()

        # TODO: open up the destination folder so that you can see your files

    """
    Set the source directory on button callback
    """
    def get_source_directory(self):
        self.source_directory = filedialog.askdirectory(title=SELECT_SOURCE_FOLDER_MESSAGE, mustexist=True)
        self.source_directory_label[TEXT_KEY] = SOURCE_DIRECTORY_FORMAT.format(self.source_directory)

    """
    Set the destination directory on button callback
    """
    def get_destination_directory(self):
        self.destination_directory = filedialog.askdirectory(title=SELECT_DESTINATION_FOLDER_MESSAGE, mustexist=True)
        self.destination_directory_label[TEXT_KEY] = DESTINATION_DIRECTORY_FORMAT.format(self.destination_directory)

    """
    Perform the actual pdf merging
    """
    def combine_the_pdfs(self):
        if self.destination_directory is None:
            messagebox.showerror(SELECT_DESTINATION_FOLDER_MESSAGE, "You must select a folder to save the pdfs in!")
        elif self.source_directory is None:
            messagebox.showerror(SELECT_SOURCE_FOLDER_MESSAGE, "You must select a folder to read the pdfs from!")
        else:
            result_files = pdfcombiner.combine_all_pdfs(self.source_directory, self.destination_directory)
            if len(result_files) > 0:
                messagebox.showinfo("Success!", "We have successfully written combined pdf files to: {}".
                                    format(self.destination_directory))
            else:
                messagebox.showwarning("No pdfs found!", "We were not able to find any pdfs to combine in {}"
                                       .format(self.source_directory))


window = tk.Tk()
pdf_combiner_gui = PdfCombiner(window)
window.mainloop()
