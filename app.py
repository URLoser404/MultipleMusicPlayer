from flask import *
from threading import Thread
import search




app = Flask(__name__)


@app.route('/' , methods=['POST','GET'])
def main():

    if request.method == "POST":
        video = search.string_search(request.form["test"])
        import pprint
        pprint.pprint(vars(video))
        search.play(video.url)

    
        return render_template("index.html",test=request.form["test"])
    
    return  render_template("index.html")


    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
