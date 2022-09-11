winget install -e --id VideoLAN.VLC
winget install -e --id Python.Python.3
winget install --id Git.Git -e --source winget

pip install -r requirements.txt

python app.py