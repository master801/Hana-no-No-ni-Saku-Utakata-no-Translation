@echo off

echo ARE YOU SURE??!!!
pause

rmdir /S /Q "WORKING\patch2\image"
rmdir /S /Q "WORKING\patch2\uipsd"

xcopy /S /Y /I "ORIGINAL\patch2\image" "WORKING\patch2\image"
xcopy /S /Y /I "ORIGINAL\patch2\uipsd" "WORKING\patch2\uipsd"

python DECODE.py
