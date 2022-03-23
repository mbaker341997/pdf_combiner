import os
import shutil
from business import mover

TEST_DIR = os.path.join('tests', 'mover_files')
PREFIX_1 = '1234567'
PREFIX_2 = '7654321'
INVALID_PREFIX = '765432'
SUFFIX_1 = '1'
SUFFIX_2 = '2'
CONTENT_1 = 'foo'
CONTENT_2 = 'bar'
PERIOD_DELIM = '.'
DASH_DELIM = '-'
UNDERSCORE_DELIM = '_'
INVALID_DELIM = 'mm'


def setup_function():
    # Create the destination if it doesn't exist
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)


def teardown_function():
    # clean up our output directory
    shutil.rmtree(TEST_DIR)
    print()


def create_files(delim):
    print()
    create_files_for_prefix(delim, PREFIX_1)
    create_files_for_prefix(delim, PREFIX_2)


def create_files_for_prefix(delim, prefix):
    create_file(get_filename(prefix, delim, SUFFIX_1), CONTENT_1)
    create_file(get_filename(prefix, delim, SUFFIX_2), CONTENT_2)


def get_filename(prefix, delim, suffix):
    return f'{prefix}{delim}{suffix}.txt'


def create_file(filename, content):
    with open(f'{TEST_DIR}/{filename}', 'w') as f:
        f.write(content)


def test_mover_moves_files_period_delim():
    create_files(PERIOD_DELIM)
    mover.move_files(TEST_DIR)
    children = os.listdir(TEST_DIR)

    # two sub-directories
    assert len(children) == 2
    assert PREFIX_1 in children
    assert PREFIX_2 in children

    validate_subdir(PREFIX_1, PERIOD_DELIM)
    validate_subdir(PREFIX_2, PERIOD_DELIM)


def test_mover_moves_files_underscore_delim():
    create_files(UNDERSCORE_DELIM)
    mover.move_files(TEST_DIR)
    children = os.listdir(TEST_DIR)

    # two sub-directories
    assert len(children) == 2
    assert PREFIX_1 in children
    assert PREFIX_2 in children

    validate_subdir(PREFIX_1, UNDERSCORE_DELIM)
    validate_subdir(PREFIX_2, UNDERSCORE_DELIM)


def test_mover_moves_files_dash_delim():
    create_files(DASH_DELIM)
    mover.move_files(TEST_DIR)
    children = os.listdir(TEST_DIR)

    # two sub-directories
    assert len(children) == 2
    assert PREFIX_1 in children
    assert PREFIX_2 in children

    validate_subdir(PREFIX_1, DASH_DELIM)
    validate_subdir(PREFIX_2, DASH_DELIM)


def test_mover_skips_files_invalid_delim():
    create_files(INVALID_DELIM)
    mover.move_files(TEST_DIR)
    children = os.listdir(TEST_DIR)

    # none of the files were moved
    assert len(children) == 4
    assert get_filename(PREFIX_1, INVALID_DELIM, SUFFIX_1) in children
    assert get_filename(PREFIX_1, INVALID_DELIM, SUFFIX_2) in children
    assert get_filename(PREFIX_2, INVALID_DELIM, SUFFIX_1) in children
    assert get_filename(PREFIX_2, INVALID_DELIM, SUFFIX_2) in children


def test_mover_skips_files_invalid_prefix():
    create_files_for_prefix(PERIOD_DELIM, INVALID_PREFIX)
    mover.move_files(TEST_DIR)
    children = os.listdir(TEST_DIR)

    # none of the files were moved
    assert len(children) == 2
    assert get_filename(INVALID_PREFIX, PERIOD_DELIM, SUFFIX_1) in children
    assert get_filename(INVALID_PREFIX, PERIOD_DELIM, SUFFIX_2) in children


def test_mover_mixed_valid_and_invalid_prefix():
    create_files_for_prefix(PERIOD_DELIM, INVALID_PREFIX)
    create_files_for_prefix(PERIOD_DELIM, PREFIX_1)
    mover.move_files(TEST_DIR)
    children = os.listdir(TEST_DIR)

    # 2 files were moved and two werent
    assert len(children) == 3
    assert PREFIX_1 in children
    assert get_filename(INVALID_PREFIX, PERIOD_DELIM, SUFFIX_1) in children
    assert get_filename(INVALID_PREFIX, PERIOD_DELIM, SUFFIX_2) in children

    # validate our one subdirectory
    validate_subdir(PREFIX_1, PERIOD_DELIM)


def test_mover_mixed_valid_and_invalid_delim():
    create_files_for_prefix(PERIOD_DELIM, PREFIX_1)
    create_files_for_prefix(INVALID_DELIM, PREFIX_1)
    mover.move_files(TEST_DIR)
    children = os.listdir(TEST_DIR)

    # 2 files were moved and two weren't
    assert len(children) == 3
    assert PREFIX_1 in children
    assert get_filename(PREFIX_1, INVALID_DELIM, SUFFIX_1) in children
    assert get_filename(PREFIX_1, INVALID_DELIM, SUFFIX_2) in children

    # validate our one subdirectory
    validate_subdir(PREFIX_1, PERIOD_DELIM)


def validate_subdir(prefix, delim):
    # get children of the subdir
    subdir = os.path.join(TEST_DIR, prefix)
    children = os.listdir(subdir)

    # the two files are in there
    assert len(children) == 2
    filename_1 = get_filename(prefix, delim, SUFFIX_1)
    filename_2 = get_filename(prefix, delim, SUFFIX_2)
    assert filename_1 in children
    assert filename_2 in children

    # files have the right content
    validate_file_content(os.path.join(subdir, filename_1), CONTENT_1)
    validate_file_content(os.path.join(subdir, filename_2), CONTENT_2)


def validate_file_content(filename_and_path, content):
    with open(filename_and_path) as f:
        assert content == f.read()
