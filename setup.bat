winget install -e --id VideoLAN.VLC
winget install -e --id Python.Python.3
winget install --id Git.Git -e --source winget

pip install requests
pip install bs4
pip install git+https://github.com/Cupcakus/pafy
pip install youtube-dl
pip install python-vlc
pip install sqlite3
pip install flask
pip install flask-cors

python execDB.py
python app.py