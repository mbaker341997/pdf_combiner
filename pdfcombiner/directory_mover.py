import os
import re
import time
import shutil

directory_string = '/home/mattbaker/coding_projects/filecombiner/test_files'
output_directory_name = f'/home/mattbaker/coding_projects/filecombiner/test_files/test_output_{time.time_ns()}'
folders = set()
os.mkdir(output_directory_name)
prefixPattern = re.compile(r'^\w{7}(?=[\.|-|_])')
with os.scandir(directory_string) as it:
    for entry in it:
        if entry.is_file():
            print(f'processing file: {entry.name}')
            directory_prefix = prefixPattern.match(entry.name)
            if directory_prefix:
                # extract prefix
                prefix = directory_prefix.group()
                print(f'prefix: {prefix}')
                absolute_path = f'{output_directory_name}/{prefix}'
                # check if folder created
                if prefix in folders:
                    print(f'Folder already exists: {prefix}')
                else:
                    # create folder if not already there
                    print(f'Creating new folder: {prefix}')
                    os.mkdir(absolute_path)
                    folders.add(prefix)
                # copy file to folder
                print(f'Moving file {entry.path} to folder {absolute_path}')
                shutil.copyfile(entry.path, f'{absolute_path}/{entry.name}')
                print(f'Successfully moved file {entry.name}')
            else:
                print(f'Filename did not match pattern: {entry.name}')
