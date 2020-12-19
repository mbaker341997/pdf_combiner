import os
import fitz
from pdfcombiner import combiner
import shutil


TEST_INPUT_DIR = os.path.join('tests', 'input_files')

TEST_EMPTY_PATH = os.path.join('tests', 'input_files', 'empty_dir')
TEST_EMPTY_DIR_FILENAME = 'empty_dir.pdf'

TEST_SUB_DIR_1_PATH = os.path.join('tests', 'input_files', 'sub_dir_1')
TEST_SUB_DIR_1_FILENAME = 'sub_dir_1.pdf'

TEST_SUB_DIR_2_PATH = os.path.join('tests', 'input_files', 'sub_dir_2')
TEST_SUB_DIR_2_FILENAME = 'sub_dir_2.pdf'

TEST_SUB_DIR_3_PATH = os.path.join('tests', 'input_files', 'sub_dir_3')
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
    pdfs = combiner.get_files_to_merge_in_dir(TEST_SUB_DIR_2_PATH)
    assert len(pdfs) == 2
    assert os.path.join(TEST_SUB_DIR_2_PATH, 'testpdf5.pdf') in pdfs
    assert os.path.join(TEST_SUB_DIR_2_PATH, 'testpdf6.pdf') in pdfs


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
    files_to_merge = combiner.get_files_to_merge_in_dir(TEST_SUB_DIR_3_PATH, 
                                                        include_jpg=False,
                                                        include_xps=True)
    assert len(files_to_merge) == 3
    assert os.path.join(TEST_SUB_DIR_3_PATH, 'testpdf7.pdf') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_3_PATH, 'multipage.xps') in files_to_merge
    assert os.path.join(TEST_SUB_DIR_3_PATH, 'singlepage.xps') in files_to_merge


def test_get_child_dirs():
    child_directories = combiner.get_child_dirs(TEST_INPUT_DIR)
    assert len(child_directories) == 4
    assert TEST_SUB_DIR_1_PATH in child_directories
    assert TEST_SUB_DIR_2_PATH in child_directories
    assert TEST_SUB_DIR_3_PATH in child_directories
    assert TEST_EMPTY_PATH in child_directories


def test_combine_docs_in_directory_skips_empty_directory():
    result = combiner.combine_docs_in_directory(TEST_EMPTY_PATH, TEST_OUTPUT_DIR)
    assert result == None


def test_combine_docs_in_directory_skips_sub_directories():
    result = combiner.combine_docs_in_directory(TEST_SUB_DIR_2_PATH, TEST_OUTPUT_DIR)
    assert result == TEST_SUB_DIR_2_FILENAME
     # contains 5 and 6
    validate_pdf_file(TEST_SUB_DIR_2_FILENAME, num_pages=2)


def test_combine_docs_in_directory_pdf_only():
    result = combiner.combine_docs_in_directory(TEST_SUB_DIR_1_PATH, TEST_OUTPUT_DIR, include_jpg=False, include_xps=False)

    assert result == TEST_SUB_DIR_1_FILENAME
    # contains 3 and 4
    validate_pdf_file(TEST_SUB_DIR_1_FILENAME, num_pages=2)


def test_combine_docs_in_directory_image_conversion():
    result = combiner.combine_docs_in_directory(TEST_SUB_DIR_1_PATH, TEST_OUTPUT_DIR, include_jpg=True, include_xps=False)

    assert result == TEST_SUB_DIR_1_FILENAME
    # contains 3, 4, basic, basicJPEG, BIG, and color
    validate_pdf_file(TEST_SUB_DIR_1_FILENAME, num_pages=6)


def test_combine_docs_in_directory_xps_conversion():
    result = combiner.combine_docs_in_directory(TEST_SUB_DIR_3_PATH, TEST_OUTPUT_DIR, include_jpg=False, include_xps=True)

    assert result == TEST_SUB_DIR_3_FILENAME
    # sub_dir_1 contains 7, singlepage.xps, and multipage.xps (which has 2 pages)
    validate_pdf_file(TEST_SUB_DIR_3_FILENAME, num_pages=4)


def teardown_function():
    # clean up our output directory
    shutil.rmtree(TEST_OUTPUT_DIR)


# This only validates the number of pages. fitz should be able to handle the combination correctly
def validate_pdf_file(file_name, num_pages):
    doc = fitz.open(os.path.join(TEST_OUTPUT_DIR, file_name))
    print(len(doc))
    assert len(doc) == num_pages
