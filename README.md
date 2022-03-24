## PDF Handler

Uses tkinter, and [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/document.html)

## PDF Combiner
Purpose:
* Given a folder filled with pdfs, merge all the pdfs into one
* Merged pdf filename will be the same as the directory name (so all the
pdfs in folder A will be merged into A.pdf)

Assumptions
* order doesn't matter
* "Children, but no grandchildren",
sub-directories will also be merged into pdfs, but will only go one layer
deep. Example, specifying starting point directory "A" as input:  

```
A
|
|--- 0.pdf
|
|--- B
|    |--- 1.pdf
|    |--- 2.pdf
|
|--- C
     |--- D
         |--- 3.pdf
```

Will produce the following

* "A.pdf" - containing the content of 0.pdf
* "B.pdf" - containing the content of 1.pdf and 2.pdf combined

It will not merge 3.pdf into anything because after looking in C
and finding no pdfs, we don't dig deeper. This is to avoid wasting
time going down a rabbit hole. I'm willing to change this in the
future perhaps, but for now keeping it simple.

DEMO VIDEO: [https://www.youtube.com/watch?v=4EEbaHv9m1o](https://www.youtube.com/watch?v=4EEbaHv9m1o)

## File Mover
Purpose:
* Move all files with 7 character prefix + delimiter of `.`, `-`, `_` in a given directory
into a subdirectory titled after the prefix
* For example, in a directory with files `1234567.1.txt`, `1234567.2.txt`, and `7654321.txt`, after
running this program, the directory will now have two subdirectories
  * Subdirectory titled `1234567` with files `1234567.1.txt`, `1234567.2.txt`
  * Subdirectory titled `7654321` with files `7654321.1.txt`

DEMO VIDEO: coming soon!

## Running
Create a venv inside of the root of the project (venv should be a child directory of pdfcombiner)
```
python -m venv venv
```

Activate it 
```
source venv/bin/activate
```

or on windows
```
venv\Scripts\activate.bat
```

Install the requirements (optionally upgrade some dependencies by adding `--upgrade` flag):
```
pip install -r requirements.txt
```

For testing, execute the following from the project root.
```
python -m pytest -s
```

This will combine the test pdfs, validate that the page amounts are what
we want, and then clean up. It also performs some tests of the file mover


Then execute the file for the GUI:
```
python root_gui.py
```

I also made an executable for windows via [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/usage.html)
```
pyinstaller root_gui.py -n pdfhandler -F -w -i assets\pdfc_icon.ico
```

## Releases

[v1.0 (win_64)](https://github.com/mbaker341997/pdf_combiner/releases/tag/v1.0)

[v1.1 (win_64)](https://github.com/mbaker341997/pdf_combiner/releases/tag/v1.1)

[v2.0 (win_64)](https://github.com/mbaker341997/pdf_combiner/releases/tag/v2.0)
