import os
import re
import shutil

# 7 characters and a dot, dash, or hyphen
PREFIX_PATTERN = re.compile(r'^\w{7}(?=[\.\-_])')


def move_files(directory_string, progress_var=None):
    folders = set()
    with os.scandir(directory_string) as it:
        for entry in it:
            if entry.is_file():
                directory_prefix = PREFIX_PATTERN.match(entry.name)
                if directory_prefix:
                    # extract prefix
                    prefix = directory_prefix.group()
                    absolute_path = f'{directory_string}/{prefix}'
                    # check if folder processed
                    if prefix not in folders:
                        # create folder if not already there
                        if not os.path.exists(absolute_path):
                            os.mkdir(absolute_path)
                            folders.add(prefix)
                    # copy file to folder
                    shutil.move(entry.path, f'{absolute_path}/{entry.name}')
                else:
                    print(f'Filename did not match pattern: {entry.name}')
            if progress_var:
                progress_var.set(progress_var.get() + 1)
