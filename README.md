# mcs-tools

This repository contains a program to process a .csv file using a .txt file that stores replacement templates.

### Type of file with replacement templates "template.txt"

The data in the `template.txt` is presented as follows

``` 
'word' 'what_to_replace'
```

If the word has the replacement pattern "delete", then the word is placed in a file named DELETE:
``` 
'word' 'delete'
```

### main.py

The program is a graphical application with three buttons:
1. Search and select files in a directory
2. Search and select a template
3. Program start

Information about file processing is displayed in a text box.

For processed .csv files, an output folder is created with the time the file processing started. Three files are created for each .csv file:
1. Bottom
2. Top
3. Delete

