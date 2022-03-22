from tkinter import ttk

TITLE_STYLE_KEY = 'Title.TLabel'
HEADING_STYLE_KEY = 'Heading.TLabel'
HELP_STYLE_KEY = 'HelpBody.TLabel'


def init_styles():
    style = ttk.Style()
    style.configure(TITLE_STYLE_KEY, font='helvetica 24')
    style.configure(HEADING_STYLE_KEY, font='helvetica 20')
    style.configure(HELP_STYLE_KEY, font='helvetica 12')
