# EpisodeMover
Console-based program to move downloaded episodes of a TV show to the proper folder

The program lets you create a database of show keywords ("X files") and the directory those shows belong in ("C:\video\X files"). 

Shows can be added, and the list of shows is saved in data.json for future use.

When needed, the user can run the mover utility to move all files/folders matching the keywords and containing the text "S##E##" from the source directory (e.g. Downloads folder) to the specified destination directory.

For example: 'X-Files S01E05' will be moved from 'C:\user\downloads\' to the specified X-Files folder 'C:\video\X files\'

Tested on Windows, though it should work on other operating systems.
