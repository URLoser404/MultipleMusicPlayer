from flask import *
from flask_cors import CORS
from threading import Thread

from sqlite3 import *

import search

current = None

import vlc

Instance = vlc.Instance()
player = Instance.media_player_new()

app = Flask(__name__)
CORS(app)



@app.route('/addSong' , methods=['POST','GET'])
def addSong():
    string = request.args.get('string')

    if string.startswith("https://www.youtube.com") :
        video = search.url_search(string)
    else:
        video = search.string_search(string)


    conn = connect('music.db')
    conn.execute(f'''insert into playlist(title,author,duration,url,img,played) values(
                    '{video.title}',
                    '{video.author}',
                    '{video.duration}',
                    '{video.watchv_url}',
                    '{video.thumb}',
                    0
                )''')
    conn.commit()

    return {
        'title' : video.title,
        'author' : video.author,
        'duration' : video.duration,
        'url' : video.watchv_url,
        'img' : video.thumb,
        'description' :video._ydl_info.get('description')
    }
    
@app.route('/playlist', methods=['POST','GET'])
def playlist():
    conn = connect('music.db')
    def dict_factory(cursor, row):
        dict = {}
        for idx, col in enumerate(cursor.description):
            dict[col[0]] = row[idx]
        return dict
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('select * from playlist')
    return jsonify(cursor.fetchall())


status = True
@app.route('/pause' , methods = ['GET','POST'])
def pause():
    global status
    if status:
        status = False
        player.pause()
    else:
        status = True
        player.play()
    return {
        'status' : status
    }

@app.route('/now', methods=['POST','GET'])
def now():
    current['position'] = (player.get_time() / 1000 ) 
    current['volume'] = player.audio_get_volume() 
    return current

@app.route('/next',methods=['POST','GET'])
def next():
    player.stop()
    return {
        'status' : status
    }
@app.route('/previous', methods=['POST','GET'])
def previous():
    conn = connect('music.db')
    conn.execute(f"update playlist set played = 0 where id = {current['id']};")
    conn.execute(f"update playlist set played = 0 where id = {current['id']-1};")
    conn.commit()
    player.stop()

    return {
        'status' : status
    }

@app.route('/volume' , methods=['POST','GET'])
def volume():
    volume = request.args.get("volume")

    player.audio_set_volume(int(volume))
    return {
        'status' : status
    } 

def run():
    app.run(host='0.0.0.0', port=8080)


server = Thread(target=run)

if __name__ == '__main__':
    
    server.start()
    while True:

        conn = connect('music.db')
        def dict_factory(cursor, row):
            dict = {}
            for idx, col in enumerate(cursor.description):
                dict[col[0]] = row[idx]
            return dict
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("select * from playlist where played = 0")


        playlist = cursor.fetchall()
        if len(playlist) != 0:
            current = playlist[0]
            print(current)
            video = search.url_search(current['url'])
            
            Media = Instance.media_new(video.getbestaudio().url)
            Media.get_mrl()
            player.set_media(Media)
            player.play()

            conn.execute(f"update playlist set played = 1 where id = {current['id']}")
            conn.commit()

            current_state = player.get_state()
            while current_state != 5 and current_state != 6:
                current_state = player.get_state() 
        else:
            print("no song")
            import time
            time.sleep(1)