@echo off
py -m pip install -r requirements-dev.txt
py -m pytest
pause
