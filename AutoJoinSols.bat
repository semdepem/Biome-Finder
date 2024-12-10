@echo off
REM Change directory to the location of your Python script
cd /d "Your\Python\Script\Location"

REM Run the Python script and minimize the command prompt window
start /min pythonw main.py

REM Close the command prompt window
exit