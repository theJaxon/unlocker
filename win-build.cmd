@echo on
rd /s /q build
rd /s /q dist
del *.spec
pyinstaller --onefile dumpsmc.py
pyinstaller --onefile gettools.py
pyinstaller --onefile unlocker.py
xcopy /y dist\*.exe .
rd /s /q build
rd /s /q dist
del *.spec