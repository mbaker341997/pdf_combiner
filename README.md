## PDF Combiner

Uses tkinter and PyPDF2

Activate the venv 
```
. venv/bin/activate
```

then run the files

Right now it's just a playground


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