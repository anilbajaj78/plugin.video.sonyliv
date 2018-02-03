from BeautifulSoup import BeautifulSoup
import os.path 
import sys
import urlparse
import json
import xbmcplugin
import urllib
from resources.lib import helpers as h

currentDisplayCounter = 0

# 

# Version 2.0.0

SHOW_BASE_URL = "https://www.sonyliv.com/"
SHOW_EPISODE_URL = SHOW_BASE_URL + "api/v2/vod/search"


# Serials
# By Mode : , Main_Branch, Defined Mode : Channel
# By Mode : Channel, show_serial, Defined Mode : episode

def main_branch():
    v_data = "{\"searchSet\":[ {\"type\":\"search\", \"pageSize\":50, \"pageNumber\":" + str(param1) + ", \"id\":\"Episodes\", \"sortOrder\":\"START_DATE:DESC\", \"data\":\"all=type:show\" }],\"detailsType\":\"basic\", \"deviceDetails\":{\"mfg\":\"Google Chrome\", \"os\":\"others\", \"osVer\":\"XXX\", \"model\":\"Google Chrome\"}}"
    xbmc.log("main_branch")
    
    JSONObjs = json.loads(h.make_request_post(SHOW_EPISODE_URL, v_data, cookie_file, cookie_jar, TOKEN))

    for rows in JSONObjs[0]["assets"]:
        title = rows["title"]
        showname = rows["showname"]
        img_src = rows["thumbnailUrl"]

        h.add_dir(addon_handle, base_url, title, showname, "episodemenu~0", img_src, rows["posterUrl"])

    currentDisplayCounter = int(param1)
    if len(JSONObjs[0]["assets"]) >= 50 :
        currentDisplayCounter = currentDisplayCounter + 1
        h.add_dir(addon_handle, base_url, 'Next >>', "Next >>", 'main~' + str(currentDisplayCounter))
    elif len(JSONObjs[0]["assets"]) < 50 :
        currentDisplayCounter = -1

def show_episodes():
    xbmc.log("Show Episodes Menu")
    showname = h.extract_var(args, 'url')

    v_data = "{\"detailsType\":\"basic\",\"searchSet\":[{\"pageSize\":50,\"pageNumber\":" + param1 + ",\"sortOrder\":\"START_DATE:DESC\",\"type\":\"search\",\"id\":\"Episodes\",\"data\":\"exact=true&all=type:Episodes&all=showname:" + showname + "\"}, {\"pageSize\":50,\"pageNumber\":" + param1 + ",\"sortOrder\":\"START_DATE:DESC\",\"type\":\"search\",\"id\":\"video\",\"data\":\"exact=true&all=type:video&all=showname:" + showname + "\"}],\"deviceDetails\":{\"mfg\":\"Google Chrome\",\"os\":\"others\",\"osVer\":\"XXX\",\"model\":\"Google Chrome\"}}"
    
    JSONObjs = json.loads(h.make_request_post(SHOW_EPISODE_URL, v_data, cookie_file, cookie_jar, TOKEN))

    for searchSet in JSONObjs:
        for rows in searchSet["assets"]:
            title = rows["title"].encode('utf-8') #+ " (" + rows["releaseDate"].encode('utf-8') + ")"
            img_src = rows["thumbnailUrl"]
            h.add_dir_video(addon_handle, title, rows["hlsUrl"], img_src, rows["shortDesc"])

    currentDisplayCounter = int(param1)
    if len(JSONObjs[0]["assets"]) >= 50 :
        currentDisplayCounter = currentDisplayCounter + 1
        h.add_dir(addon_handle, base_url, 'Next >>', showname, "episodemenu~" + str(currentDisplayCounter))
    elif len(JSONObjs[0]["assets"]) < 50 :
        currentDisplayCounter = -1

addon_id = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
cookie_file, cookie_jar, TOKEN = h.init_cookie_jar(addon_id)

base_url = sys.argv[0]

addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
params = args.get('mode', ['', ])[0].split("~")

param1 = 0
param2 = ""

mode = params[0]
if len(params) >= 2:
    param1 = params[1]
if len(params) >= 3:
    param2 = params[2]


if mode == 'episodemenu':
    show_episodes()
else:
    main_branch()

xbmcplugin.endOfDirectory(addon_handle)
