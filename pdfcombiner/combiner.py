from os import path, scandir
import fitz

PDF_EXTENSION = ".pdf"
XPS_EXTENSION = ".xps"
JPG_EXTENSION = ".jpg"
JPEG_EXTENSION = ".jpeg" # what a disaster for the human race


# returns filenames with path of all pdf files in directory
# optionally include jpg and xps files too
def get_files_to_merge_in_dir(directory, include_jpg=False, include_xps=False):
    extension_set = {PDF_EXTENSION}
    if include_jpg:
        extension_set.update([JPG_EXTENSION, JPEG_EXTENSION])
    if include_xps:
        extension_set.update([XPS_EXTENSION])
    files = []
    with scandir(directory) as it:
        for entry in it:
            if entry.is_file():
                if path.splitext(entry.name)[1] in extension_set:
                    files.append(path.join(directory, entry.name))
    return files


def get_child_dirs(root_directory):
    child_dirs = []
    with scandir(root_directory) as it:
        for entry in it:
            if entry.is_dir():
                child_dirs.append(path.join(root_directory, entry.name))
    return child_dirs


def convert_to_pdf(input_filepath):
    print("Converting: {} to pdf".format(input_filepath))
    input_doc = fitz.open(input_filepath)
    return input_doc.convertToPDF()


# Given a directory, find all its eligible documents and merge
def combine_docs_in_directory(source_directory, destination_path, include_jpg=False, include_xps=False, progress_var=None):
    output_filename = "{}.pdf".format(path.split(source_directory)[1])
    print("Reading pdfs from: {}".format(source_directory))
    files_to_merge = get_files_to_merge_in_dir(source_directory, include_jpg, include_xps)
    if len(files_to_merge) > 0:
        print("Writing combined file: {}".format(output_filename))
        merged_file = fitz.open()
        for file_to_merge in files_to_merge:
            fitz_file_to_merge = fitz.open(file_to_merge)
            # if file isn't a pdf, then convert to bytes
            if not fitz_file_to_merge.isPDF:
                print("Converting: {} to pdf".format(file_to_merge))
                converted_file_bytes = fitz_file_to_merge.convertToPDF()
                converted_file = fitz.open("pdf", converted_file_bytes)
                merged_file.insertPDF(converted_file)
            else:
                merged_file.insertPDF(fitz_file_to_merge)
            fitz_file_to_merge.close()
            if progress_var:
                progress_var.set(progress_var.get() + 1)
        merged_file.save(path.join(destination_path, output_filename))
        merged_file.close()
        print("Successfully written: {}".format(output_filename))
        result = output_filename
    else:
        print("No pdf files found in {}, skipping".format(source_directory))
        result = None
    return result


# given a root directory, combine all the pdfs in each of its sub-directories (first layer only)
def combine_all_docs(root_directory, destination_path, include_jpg=False, include_xps=False):
    print("Combining all pdfs in {}".format(root_directory))
    result_files = []

    # combine pdfs in root
    root_file = combine_docs_in_directory(root_directory, destination_path, include_jpg, include_xps)
    if root_file:
        result_files.append(root_file)

    # combine pdfs in first layer of children
    for child_dir in get_child_dirs(root_directory):
        result_file = combine_docs_in_directory(child_dir, destination_path,  include_jpg, include_xps)
        if result_file:
            result_files.append(result_file)

    # print results to stdout
    print("Finished combining all pdfs. Written files: ")
    for result_file in result_files:
        print("* {}".format(result_file))
    return result_files
