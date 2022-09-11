def url_search(url):
    
    import pafy
    video = pafy.new(url)

    return video


def string_search(search):

    import re, requests, subprocess, urllib.parse, urllib.request
    from bs4 import BeautifulSoup

    query_string = urllib.parse.urlencode({"search_query": search})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    url =  "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])

    return url_search(url)


def play(url):

    
    import vlc

    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(url)
    Media.get_mrl()
    player.set_media(Media)
    player.play()


if __name__ == "__main__":
    video = url_search("https://www.youtube.com/watch?v=a7t62tOIhvE")
    import pprint
    print(video.getbestvideo().url)





