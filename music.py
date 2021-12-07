# import vlc

# # print(playurl)

# Instance = vlc.Instance()
# player = Instance.media_player_new()
# Media = Instance.media_new(playurl)

# Media.get_mrl()
# player.set_media(Media)
# player.play()
def url_play(url):
    import pafy
    video = pafy.new(url)
    print(video)
    best = video.getbest()
    
    playurl = best.url

    return playurl


def search(search):
    import re, requests, subprocess, urllib.parse, urllib.request
    from bs4 import BeautifulSoup

    query_string = urllib.parse.urlencode({"search_query": search})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    return "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])

url_play(search("我站在雲林"))


# subprocess.Popen(
# "start /b " + "path\\to\\mpv.exe " + clip2 + " --no-video --loop=inf --input-ipc-server=\\\\.\\pipe\\mpv-pipe > output.txt",
# shell=True)


# Alternatively, you can do this for simplicity sake:
# subprocess.Popen("start /b " + "path\\to\\mpv.exe " + clip2 + "--no-video", shell=True)
