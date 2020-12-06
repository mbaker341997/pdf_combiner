from PyPDF2 import PdfFileMerger
from os import path, scandir

PDF_EXTENSION = ".pdf"


# returns filenames with path of all .pdf files in the given directory
def get_pdfs_in_dir(directory):
    files = []
    with scandir(directory) as it:
        for entry in it:
            if entry.is_file():
                if path.splitext(entry.name)[1] == PDF_EXTENSION:
                    files.append(path.join(directory, entry.name))
    return files


def get_child_dirs(root_directory):
    child_dirs = []
    with scandir(root_directory) as it:
        for entry in it:
            if entry.is_dir():
                child_dirs.append(path.join(root_directory, entry.name))
    return child_dirs


# Given a directory, find all its pdfs and merge
def combine_pdfs_in_directory(source_directory, destination_path):
    merger = PdfFileMerger()
    output_filename = "{}.pdf".format(path.split(source_directory)[1])
    print("Reading pdfs from: {}".format(source_directory))
    pdfs = get_pdfs_in_dir(source_directory)
    for pdf in pdfs:
        print("Merging file {}".format(pdf))
        merger.append(pdf)
    if len(pdfs) > 0:
        print("Writing combined file: {}".format(output_filename))
        with open(path.join(destination_path, output_filename), "wb") as output_file:
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
    print("Combining all pdfs in {}".format(root_directory))
    result_files = []

    # combine pdfs in root
    root_file = combine_pdfs_in_directory(root_directory, destination_path)
    if root_file:
        result_files.append(root_file)

    # combine pdfs in first layer of children
    for child_dir in get_child_dirs(root_directory):
        result_file = combine_pdfs_in_directory(child_dir, destination_path)
        if result_file:
            result_files.append(result_file)

    # print results to stdout
    print("Finished combining all pdfs. Written files: ")
    for result_file in result_files:
        print("* {}".format(result_file))
    return result_files
