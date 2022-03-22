import os
import re
import shutil
import time

# 7 characters and a dot, dash, or hyphen
PREFIX_PATTERN = re.compile(r'^\w{7}(?=[\.|-|_])')


def move_files(directory_string):
    folders = set()
    output_directory = f'{directory_string}/output_{time.time_ns()}'
    os.mkdir(output_directory)
    with os.scandir(directory_string) as it:
        for entry in it:
            if entry.is_file():
                directory_prefix = PREFIX_PATTERN.match(entry.name)
                if directory_prefix:
                    # extract prefix
                    prefix = directory_prefix.group()
                    absolute_path = f'{output_directory}/{prefix}'
                    # check if folder created
                    if prefix not in folders:
                        # create folder if not already there
                        os.mkdir(absolute_path)
                        folders.add(prefix)
                    # copy file to folder
                    shutil.copyfile(entry.path, f'{absolute_path}/{entry.name}')
                else:
                    print(f'Filename did not match pattern: {entry.name}')
