@REM Used to copy working files to the modified folder to use later when packing the xp3 file
@REM Created by Master801
@REM Encodes translation scripts and copies game files to prepare for repacking

@REM Moved batch script to pure Python because Windows can't handle it...
TITLE ENCODE
python ENCODE.py --compile --process_scn