del __main__.spec
del .\dist\__main__.exe
rmdir /S /Q build
%appdata%\Python\Python37\Scripts\pyinstaller.exe --onefile --icon=./assets/icon.ico ./src