# import vlc

# # print(playurl)

# Instance = vlc.Instance()
# player = Instance.media_player_new()
# Media = Instance.media_new(playurl)

# Media.get_mrl()
# player.set_media(Media)
# player.play()
class music:
    def __init__(self,video,url,playurl):
        self.title = video.Title
        self.author = video.Author
        self.yt_code = video.ID
        self.duration = video.Duration
        self.rating = video.Rating
        self.views = video.Views
        self.thumbnail = video.Thumbnail
        self.url = url
        self.playurl = playurl



def url_search(url):
    import pafy
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url

    return best


def string_search(search):
    import re, requests, subprocess, urllib.parse, urllib.request
    from bs4 import BeautifulSoup

    query_string = urllib.parse.urlencode({"search_query": search})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    url =  "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])

    return url_search(url)

    
if __name__ == "__main__":
    print(vars(string_search("殺死那個石家莊人")))



