from flask import *
from threading import Thread



import search
import execDB


playlist = []


app = Flask(__name__)


@app.route('/' , methods=['POST','GET'])
def main():

    if request.method == "POST":
        
        string = request.form["test"]
        if string.startswith("https://www.youtube.com") :
            video = search.url_search(string)
        else:
            video = search.string_search(string)

        

        print(video._parent)

        

        # execDB.exec("insert into playlist values")

        # playlist = execDB.exec("select * from playlist where ")

        # import pprint
        # pprint(playlist)

    
        return render_template("index.html",test=request.form["test"])
    
    return  render_template("index.html")


    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

    # playlist = []
    # while True:
        

        

        


