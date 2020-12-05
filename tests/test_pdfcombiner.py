import os
import pdfcombiner
import PyPDF2
import shutil


TEST_INPUT_DIR = 'tests/input_pdfs'
TEST_INPUT_PDFS_FILENAME = 'input_pdfs.pdf'

TEST_EMPTY_PATH = 'tests/input_pdfs/sub_dir_2'
TEST_EMPTY_DIR_FILENAME = 'empty_dir.pdf'

TEST_SUB_DIR_1_PATH = 'tests/input_pdfs/sub_dir_2'
TEST_SUB_DIR_1_FILENAME = 'sub_dir_1.pdf'

TEST_SUB_DIR_2_PATH = 'tests/input_pdfs/sub_dir_2'
TEST_SUB_DIR_2_FILENAME = 'sub_dir_2.pdf'

TEST_SUB_DIR_3_PATH = 'tests/input_pdfs/sub_dir_2/sub_dir_3'
TEST_SUB_DIR_3_FILENAME = 'sub_dir_3.pdf'

TEST_OUTPUT_DIR = 'tests/output_pdfs'

TEST_INPUT_PDFS = 'input_pdfs.pdf'
TEST_EMPTY_DIR_PDF = 'empty_dir.pdf'
TEST_SUB_DIR_1 = 'sub_dir_1.pdf'
TEST_SUB_DIR_2 = 'sub_dir_2.pdf'
TEST_SUB_DIR_3 = 'sub_dir_3.pdf'


# Integration tests to verify it works correctly
def test_get_child_dirs():
    child_directories = pdfcombiner.get_child_dirs(TEST_INPUT_DIR)
    assert len(child_directories) == 3
    assert TEST_SUB_DIR_1_PATH in child_directories
    assert TEST_SUB_DIR_2_PATH in child_directories
    assert TEST_SUB_DIR_3_PATH not in child_directories


def test_combine_all_pdfs():
    # I could programmatically create all my test input files, but ehhh I think it's easier to understand with the
    # files just there to be looked at
    result_files = pdfcombiner.combine_all_pdfs(TEST_INPUT_DIR, TEST_OUTPUT_DIR)

    # only 3 pdfs made
    assert len(result_files) == 3

    # input_pdfs contains 1, 2, and napoleon. Napoleon is 3 pages long so 5 pages total
    assert TEST_INPUT_PDFS_FILENAME in result_files
    validate_pdf_file(TEST_INPUT_PDFS_FILENAME, num_pages=5)

    # empty dir should not exist
    assert TEST_EMPTY_DIR_FILENAME not in result_files

    # sub_dir_1 contains 3 and 4
    assert TEST_SUB_DIR_1_FILENAME in result_files
    validate_pdf_file(TEST_SUB_DIR_1_FILENAME, num_pages=2)

    # sub_dir_2 contains 5 and 6
    assert TEST_SUB_DIR_2_FILENAME in result_files
    validate_pdf_file(TEST_SUB_DIR_2_FILENAME, num_pages=2)

    # sub_dir_3 does not exist, we don't check grandchildren
    assert TEST_SUB_DIR_3_FILENAME not in result_files

    # clean up our output directory
    shutil.rmtree(TEST_OUTPUT_DIR)


# This only validates the number of pages. PyPDF should be able to handle the combination correctly
# PageObject.extractText isn't very reliable.
# Reference: https://pythonhosted.org/PyPDF2/PageObject.html#PyPDF2.pdf.PageObject.extractText
def validate_pdf_file(file_name, num_pages):
    with open(os.path.join(TEST_OUTPUT_DIR, file_name), 'rb') as read_pdf:
        # read the pdf
        pdf = PyPDF2.PdfFileReader(read_pdf)
        # it has the number pages we expect
        assert pdf.getNumPages() == num_pages

