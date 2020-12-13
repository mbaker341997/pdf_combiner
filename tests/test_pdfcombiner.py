import os
import fitz
from pdfcombiner import combiner
import shutil


TEST_INPUT_DIR = os.path.join('tests', 'input_files')
TEST_INPUT_PDFS_FILENAME = 'input_files.pdf'

TEST_EMPTY_PATH = os.path.join('tests', 'input_files', 'empty_dir')
TEST_EMPTY_DIR_FILENAME = 'empty_dir.pdf'

TEST_SUB_DIR_1_PATH = os.path.join('tests', 'input_files', 'sub_dir_1')
TEST_SUB_DIR_1_FILENAME = 'sub_dir_1.pdf'

TEST_SUB_DIR_2_PATH = os.path.join('tests', 'input_files', 'sub_dir_2')
TEST_SUB_DIR_2_FILENAME = 'sub_dir_2.pdf'

TEST_SUB_DIR_3_PATH = os.path.join('tests', 'input_files', 'sub_dir_2', 'sub_dir_3')
TEST_SUB_DIR_3_FILENAME = 'sub_dir_3.pdf'

TEST_OUTPUT_DIR = os.path.join('tests', 'output_pdfs')

def setup_function():
    # Create the destination if it doesn't exist
    if not os.path.exists(TEST_OUTPUT_DIR):
        os.makedirs(TEST_OUTPUT_DIR)

    # Create the empty directory if it doesn't exist
    if not os.path.exists(TEST_EMPTY_PATH):
        os.makedirs(TEST_EMPTY_PATH)

def test_get_files_to_merge_base_case():
    pdfs = combiner.get_files_to_merge_in_dir(TEST_SUB_DIR_3_PATH)
    assert len(pdfs) == 1
    assert os.path.join(TEST_SUB_DIR_3_PATH, 'testpdf7.pdf') in pdfs


def test_get_files_to_merge_empty():
    pdfs = combiner.get_files_to_merge_in_dir(TEST_EMPTY_PATH)
    assert len(pdfs) == 0


def test_get_files_to_merge_does_not_include_sub_dirs():
    pdfs = combiner.get_files_to_merge_in_dir(TEST_INPUT_DIR)
    assert len(pdfs) == 3
    assert os.path.join(TEST_INPUT_DIR, 'testpdf1.pdf') in pdfs
    assert os.path.join(TEST_INPUT_DIR, 'testpdf2.pdf') in pdfs
    assert os.path.join(TEST_INPUT_DIR, 'napoleon.pdf') in pdfs


def test_get_files_to_merge_does_not_include_non_pdfs():
    pdfs = combiner.get_files_to_merge_in_dir(TEST_SUB_DIR_1_PATH)
    assert len(pdfs) == 2
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'testpdf3.pdf') in pdfs
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'testpdf4.pdf') in pdfs


def test_get_files_to_merge_will_accept_jpg_files():
    files_to_merge = combiner.get_files_to_merge_in_dir(TEST_SUB_DIR_1_PATH, 
                                                        include_jpg=True)
    assert len(files_to_merge) == 6
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'testpdf3.pdf') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'testpdf4.pdf') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'basicJPEG.jpeg') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'basic.jpg') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'BIG.jpg') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'color.jpg') in files_to_merge

def test_get_files_to_merge_will_accept_xps_files():
    files_to_merge = combiner.get_files_to_merge_in_dir(TEST_SUB_DIR_1_PATH, 
                                                        include_jpg=False,
                                                        include_xps=True)
    assert len(files_to_merge) == 4
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'testpdf3.pdf') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'testpdf4.pdf') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'multipage.xps') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_1_PATH, 'singlepage.xps') in files_to_merge


def test_get_child_dirs():
    child_directories = combiner.get_child_dirs(TEST_INPUT_DIR)
    assert len(child_directories) == 3
    assert TEST_SUB_DIR_1_PATH in child_directories
    assert TEST_SUB_DIR_2_PATH in child_directories
    assert TEST_SUB_DIR_3_PATH not in child_directories


def test_combine_all_docs_pdf_only():
    # I could programmatically create all my test input files, but ehhh I think it's easier to understand with the
    # files just there to be looked at
    result_files = combiner.combine_all_docs(TEST_INPUT_DIR, TEST_OUTPUT_DIR, include_jpg=False, include_xps=False)

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

def test_combine_all_docs_with_image_conversion():
    result_files = combiner.combine_all_docs(TEST_INPUT_DIR, TEST_OUTPUT_DIR, include_jpg=True, include_xps=False)

    # only 3 pdfs made
    assert len(result_files) == 3

    # input_pdfs contains 1, 2, and napoleon. Napoleon is 3 pages long so 5 pages total
    assert TEST_INPUT_PDFS_FILENAME in result_files
    validate_pdf_file(TEST_INPUT_PDFS_FILENAME, num_pages=5)

    # empty dir should not exist
    assert TEST_EMPTY_DIR_FILENAME not in result_files

    # sub_dir_1 contains 3, 4, basic, basicJPEG, BIG, and color
    assert TEST_SUB_DIR_1_FILENAME in result_files
    validate_pdf_file(TEST_SUB_DIR_1_FILENAME, num_pages=6)

    # sub_dir_2 contains 5 and 6
    assert TEST_SUB_DIR_2_FILENAME in result_files
    validate_pdf_file(TEST_SUB_DIR_2_FILENAME, num_pages=2)

    # sub_dir_3 does not exist, we don't check grandchildren
    assert TEST_SUB_DIR_3_FILENAME not in result_files


def test_combine_all_docs_with_xps_conversion():
    result_files = combiner.combine_all_docs(TEST_INPUT_DIR, TEST_OUTPUT_DIR, include_jpg=False, include_xps=True)

    # only 3 pdfs made
    assert len(result_files) == 3

    # input_pdfs contains 1, 2, and napoleon. Napoleon is 3 pages long so 5 pages total
    assert TEST_INPUT_PDFS_FILENAME in result_files
    validate_pdf_file(TEST_INPUT_PDFS_FILENAME, num_pages=5)

    # empty dir should not exist
    assert TEST_EMPTY_DIR_FILENAME not in result_files

    # sub_dir_1 contains 3, 4, singlepage.xps, and multipage.xps (which has 2 pages)
    assert TEST_SUB_DIR_1_FILENAME in result_files
    validate_pdf_file(TEST_SUB_DIR_1_FILENAME, num_pages=5)

    # sub_dir_2 contains 5 and 6
    assert TEST_SUB_DIR_2_FILENAME in result_files
    validate_pdf_file(TEST_SUB_DIR_2_FILENAME, num_pages=2)

    # sub_dir_3 does not exist, we don't check grandchildren
    assert TEST_SUB_DIR_3_FILENAME not in result_files


def teardown_function():
    # clean up our output directory
    shutil.rmtree(TEST_OUTPUT_DIR)


# This only validates the number of pages. fitz should be able to handle the combination correctly
def validate_pdf_file(file_name, num_pages):
    doc = fitz.open(os.path.join(TEST_OUTPUT_DIR, file_name))
    print(len(doc))
    assert len(doc) == num_pages
