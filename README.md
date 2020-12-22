# 花の野に咲くうたかたの / Hana no No ni Saku Utakata no - English Translation

![Img cover](https://s2.vndb.org/cv/21/27121.jpg)

## What is this repository about?
This repository contains text for translating the game 花の野に咲くうたかたの.<br/>
Scripts (`TRANS_TOOL/import.py`, `TRANS_TOOL/export.py`) are to extract and insert translated text into the decompiled scripts to avoid directly sharing game files.<br/>
Text is extracted from the game with patch [1.11](http://www.applique-soft.com/sapo/hananono_patch_v1_11.zip) applied.

## Repository Structure
The directory `pretty_jpn` contains readable json text lines in ***Japanese***, of the original scn json script.<br/>
The directory `pretty_eng` contains readable json text lines in ***English***, a translated copy of `pretty_jpn`.

## Instructions
### [How to unpack - Part 1](#part1)
Download and install [Python](https://www.python.org/downloads/release/python-391/)<br/>
Clone, download or fork this repository<br/>
Apply patch [1.11](http://www.applique-soft.com/sapo/hananono_patch_v1_11.zip) if not already<br/>
Download [`KrkrExtract`](#credits), extract files `KrkrExtract.exe` and `KrkrExtract.dll` to the game's directory.<br/>
Click and drag file `花の野に咲くうたかたの.exe` to file `KrkrExtract.exe`. The game and KrkrExtract windows should pop up.<br/>
Click and drag files `data.xp3` and `patch.xp3` to the KrkrExtract window. It will automatically unpack the game data. This will take a while.<br/>

----------------
### [How to decompile game text scripts - Part 2](#part2)
Open a new file explorer window and go to where you cloned, downloaded or forked the repository to.<br/>
Download [`FreeMote`](#credits) and extract folder `FreeMoteToolkit` to `ENV/TOOLS`.<br/>
Open folder `KrkrExtract_Output/data` and copy folder `scn` to `ENV/ORIGINAL/patch2`. Folder `patch2` should now have the folder `scn` in it.<br/>
Go back to the `KrkrExtract_Output` folder and go to the `patch` folder.<br/>
Copy all `.scn` files, copy and replace any files in the `ENV/ORIGINAL/patch2/scn` folder.<br/>
Run the file `DECODE`(`.bat` or `.sh`) that is in the the `ENV` folder.<br/>

Make any changes to the translation files in the `pretty_eng` folder or files in `WORKING/patch2`.<br/>

**WARNING: DO NOT** create a `scn` folder in `WORKING/patch2`. The scripts automate the process for you, so you don't need to worry about that.<br/>

----------------
### [How to recompile game text scripts - Part 3](#part3)
Open the repository folder and go into the `TRANS_TOOL` folder and run the `export.py` to translate the scripts from `pretty_eng`<br/>
Run the `ENCODE`(`.bat` or `.sh`) file that is in the `ENV` folder<br/>

----------------
### [How to repack - Part 4](#part4)
Click and drag file `花の野に咲くうたかたの.exe` to file `KrkrExtract.exe` once again.<br/>
Click and drag folder `patch2` in `ENV/MODIFIED` to repack. File `patch2.xp3` should have been created.<br/>
Move file `patch2.xp3` into the game's directory.<br/>
Run the game and see your changes.


## [Credits](#credits)
[VNDB for the cover image](https://vndb.org/v16193/)<br/>
[xmoeproject](https://github.com/xmoeproject) for [KrkrExtract](https://github.com/xmoeproject/KrkrExtract) - Used to extract game files.<br/>
[UlyssesWu](https://github.com/UlyssesWu) for [FreeMote](https://github.com/UlyssesWu/FreeMote) - Used to decompile the scn scripts
