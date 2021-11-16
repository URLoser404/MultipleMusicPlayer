from fastapi import *

app = FastAPI()



@app.get("/music/current")
def get_current():
    return {
        "current song":"song name",
        "url":"url",
        "status" : "status"
    }

@app.get("/music/queue")
def get_queue():
    return {
        "queue":[
            "song name",
            "song name"
        ]
    }

@app.post("/music/control")
def control():
    return {
        ""
    }
