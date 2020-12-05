## PDF Combiner

Uses tkinter and PyPDF2

Requirements: 
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

## Testing
From project root, run
```
python -m pytest -s
```

This will combine the test pdfs, validate that the page amounts are what 
we want, and then clean up. 

To run the gui, just do 
```
python gui.py
```

## Next Steps

Styling Changes:
* Add icon photo
* Add preview of files that will be combined (treeView)
* display of the combined files (treeView)

Convenience changes
* Add a help dialog box to explain what's happening 
* Add a CLI execution as an alternative to the GUI 

Distribution
* Make sure the setup.py is set up correctly so that module is installable
on other machines
* create linux exe 
* create windows exe 