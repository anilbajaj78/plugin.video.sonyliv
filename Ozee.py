from bs4 import BeautifulSoup
import urllib.request
import json

#soup = BeautifulSoup(open("d:\zeemarathi.html"), "html.parser")

#list = soup.find_all("div", class_="thumbnail-with-border-small-title clearfix")

#print(list)

#for div in list:
#    print("HREF : " + div.find('a')["href"])
#    print("Title : " + div.find('div').find('span')["title"])
#    print("Src : " + div.find('img')["src"])
#    print(div)

#soup = BeautifulSoup(urllib.request.urlopen("http://www.ozee.com/shos/eka-lagnachi-dusri-goshta/video"), "html.parser")

#list = soup.find_all("div", class_="col-md-3 col-xs-6 reduce-padding")
#print(list)
#for div in list:
#    print("HREF 1: " + div.find('a')["href"])
#    print("Title 1: " + div.find('img')['title'])
#    print("Src 1: " + div.find('img')['src'])
#    print("-------------------------------")


soup = BeautifulSoup(urllib.request.urlopen(" http://www.ozee.com/shows/nakshatra/video/nakshatra-episode-12-august-30-2015-full-episode.html"), "html.parser")
div = soup.find("div", id_="episode-detail-page")
list = soup.find_all("script")

for div in list:
    if 'playbackurl' in div.text:
        print(div.text.split("playbackurl = ")[1].split("\n")[0][1:-2])
    
dataJson = soup.find('script', {'type':'application/ld+json'})
data = json.loads(dataJson.text)
print("\nDescription : " + data["video"]["description"])
print("\nName : " + data["video"]["name"])
print("\nThumbnailUrl : " + data["video"]["thumbnailUrl"])
