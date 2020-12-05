import os
from PyPDF2 import PdfFileMerger, utils

PDF_EXTENSION = ".pdf"


def get_child_dirs(root_directory):
    child_dirs = []
    with os.scandir(root_directory) as it:
        for entry in it:
            if entry.is_dir():
                child_dirs.append(os.path.join(root_directory, entry.name))
    return child_dirs


# Given a directory, find all its pdfs and merge
def combine_pdfs_in_directory(source_directory, destination_path):
    merger = PdfFileMerger()
    output_filename = "{}.pdf".format(os.path.split(source_directory)[1])
    print("Reading pdfs from: {}".format(source_directory))
    num_files_merged = 0  # used to track if we have files to merge
    with os.scandir(source_directory) as it:
        for entry in it:
            if entry.is_file():
                if os.path.splitext(entry.name)[1] == PDF_EXTENSION:
                    try:
                        print("Merging file {}".format(entry.name))
                        merger.append(os.path.join(source_directory, entry.name))
                        num_files_merged += 1
                    except utils.PyPdfError:
                        print("Error combining pdfs: {}".format(output_filename))
    if num_files_merged > 0:
        print("Writing combined file: {}".format(output_filename))
        with open(os.path.join(destination_path, output_filename), "wb") as output_file:
            merger.write(output_file)
        print("Successfully written: {}".format(output_filename))
        result = output_filename
    else:
        print("No pdf files found in {}, skipping".format(source_directory))
        result = None
    merger.close()
    return result


# given a root directory, combine all the pdfs in its sub directory
def combine_all_pdfs(root_directory, destination_path):
    # Create the destination path if it doesn't exist
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    print("Combining all pdfs in {}".format(root_directory))
    result_files = [combine_pdfs_in_directory(root_directory, destination_path)]
    for child_dir in get_child_dirs(root_directory):
        result_file = combine_pdfs_in_directory(child_dir, destination_path)
        if result_file:
            result_files.append(result_file)
    print("Finished combining all pdfs. Written files: ")
    for result_file in result_files:
        print("* {}".format(result_file))
    return result_files
