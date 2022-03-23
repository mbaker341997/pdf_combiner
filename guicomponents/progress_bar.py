import queue
import threading
import tkinter as tk
from guicomponents import config
from tkinter import ttk
from utils import icon

PROGRESS_BAR_LENGTH = 300
VALUE_KEY = 'value'


class ProgressBar:
    """Construct generates a progress bar and executes a function"""

    def __init__(self,
                 parent,
                 task_func=lambda q: q.put(config.TASK_FINISHED_MESSAGE),
                 task_outcome_func_map=None,
                 progress_title="Working",
                 progress_text="Working...",
                 progress_goal=1):
        # parent frame
        self.parent = parent

        # Queue to signal when our async process is done
        self.signal_queue = queue.Queue()

        # progress bar UI
        self.progress_window = tk.Toplevel()
        self.progress_window.wm_title(progress_title)
        self.progress_window.iconphoto(self.progress_window, tk.PhotoImage(data=icon.get_pdf_icon()))
        progress_label = ttk.Label(self.progress_window, text=progress_text)
        progress_label.pack()
        self.progress_bar = ttk.Progressbar(self.progress_window,
                                            orient=tk.HORIZONTAL,
                                            length=PROGRESS_BAR_LENGTH,
                                            mode='determinate')
        self.progress_bar.pack(padx=config.PAD_X_AMOUNT, pady=config.PAD_Y_AMOUNT, fill=tk.X)
        self.progress_bar['maximum'] = PROGRESS_BAR_LENGTH
        self.progress_window.withdraw()

        # Values that we update to reflect progress
        self.progress_var = tk.IntVar(self.progress_window)
        self.progress_goal = progress_goal

        # map of message string to function to execute when that function succeeds
        if task_outcome_func_map is None:
            task_outcome_func_map = {}
        self.msg_to_func_map = task_outcome_func_map

        # function that executes asynchronously, updates progress, and puts value in signal queue when it's done
        self.task_func = task_func

    # function runs at an interval that updates the progress bar and checks signal queue to see if the task is done yet
    def process_queue(self):
        if self.progress_goal > 0:
            self.progress_bar[VALUE_KEY] = (self.progress_var.get() / self.progress_goal) * PROGRESS_BAR_LENGTH
            self.progress_window.update()
        try:
            msg = self.signal_queue.get(False)
            # clear progress value
            self.progress_var.set(0)
            self.progress_bar[VALUE_KEY] = 0
            self.progress_window.withdraw()

            # perform whatever post-execution methods are configured in queue map based on msg
            if self.msg_to_func_map[msg]:
                self.msg_to_func_map[msg]()
            else:
                print(f"No function found to execute after msg: {msg}")
        except queue.Empty:
            # nothing in signal queue yet, wait 100 ms and execute method again
            self.parent.after(100, self.process_queue)

    # Kicks off the rendering of the progress bar and the async task that updates its value.
    # Parent invokes this function, on button click, toggle, or whatever
    def perform_action(self):
        CombinerTask(self.signal_queue, self.progress_var, self.task_func).start()
        self.progress_window.deiconify()
        self.parent.after(100, self.process_queue)


class CombinerTask(threading.Thread):
    """Async task that runs with the progress bar"""

    def __init__(self, signal_queue, progress_var, task_func):
        threading.Thread.__init__(self)
        self.signal_queue = signal_queue
        self.task_func = task_func
        self.progress_var = progress_var

    def run(self):
        self.task_func(self.signal_queue, self.progress_var)
