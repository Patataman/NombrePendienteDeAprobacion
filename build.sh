pyinstaller -F --clean --workpath ../basura --hidden-import=pygame --add-data assets:assets --add-data classes/characters.json:classes main.py