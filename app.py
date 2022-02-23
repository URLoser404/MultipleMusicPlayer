import flask
import logging
from flask_cors import CORS
from threading import Thread
app = flask.Flask(__name__)
CORS(app)
log = logging.getLogger('werkzeug')
log.disabled = True
current = {}

import vlc
Instance = vlc.Instance()
player = Instance.media_player_new()


from sqlite3 import *
import search



@app.route('/')
def main():
    return flask.render_template('index.html')


@app.route('/addSong' , methods=['POST','GET'])
def addSong():
    string = flask.request.args.get('string')

    if string.startswith("https://www.youtube.com") :
        video = search.url_search(string)
    else:
        video = search.string_search(string)


    conn = connect('music.db')
    conn.execute(f'''insert into playlist(title,author,duration,url,img,music,played) values(
                    '{video.title}',
                    '{video.author}',
                    '{video.duration}',
                    '{video.watchv_url}',
                    '{video.thumb}',
                    '{video.getbestaudio().url}',
                    False
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

@app.route('/play',methods=['POST','GET'])
def play():
    id = flask.request.args.get('id')
    conn = connect('music.db')
    conn.execute(f"update playlist set played = True where id < {id}")
    conn.commit()
    conn.execute(f"update playlist set played = False where id >= {id}")
    conn.commit()
    player.stop()
    return flask.redirect('/now')
    
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
    return flask.jsonify(cursor.fetchall())


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
    current['time'] = (player.get_time() / 1000) 
    current['volume'] = player.audio_get_volume() 
    current['rate'] = player.get_rate()
    current['status'] = status
    return current
@app.route('/next',methods=['POST','GET'])
def next():
    player.stop()
    return flask.redirect('/now')
@app.route('/previous', methods=['POST','GET'])
def previous():
    conn = connect('music.db')
    conn.execute(f"update playlist set played = False where id >= {current['id']-1}")
    conn.commit()
    player.stop()
    return flask.redirect('/now')
@app.route('/volume' , methods=['POST','GET'])
def volume():
    volume = flask.request.args.get("volume")
    player.audio_set_volume(int(volume))
    return flask.redirect('/now')
@app.route('/rate' , methods=['POST','GET'])
def rate():
    rate = flask.request.args.get("rate")
    player.set_rate(float(rate))
    return flask.redirect('/now')

def run():
    app.run(host='0.0.0.0', port=8080)
    

server = Thread(target=run)

if __name__ == '__main__':
    
    import execDB 
    execDB.main()

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
        cursor.execute("select * from playlist where played = False")


        playlist = cursor.fetchall()
        if len(playlist) != 0:
            current = playlist[0]
            
            print(f"now playing : {current['title']}")

            Media = Instance.media_new(current['music'])
            Media.get_mrl()
            player.set_media(Media)
            player.play()

            conn.execute(f"update playlist set played = True where id = {current['id']}")
            conn.commit()

            current_state = player.get_state()
            while current_state != 5 and current_state != 6:
                current_state = player.get_state()
        import time
        time.sleep(1) 