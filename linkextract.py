import re
#import requests
from bs4 import BeautifulSoup
import urllib.request

def getrtmp (url):
        site = urllib.request.urlopen(url)
        soup = BeautifulSoup(site, "html.parser")
        data = soup.get_text()
        for line in data.splitlines():
                if 'rtmp' in line:
                        url = (re.findall(r'"([^"]*)"', line))
                        url = url[0]
                        return (url)

def date (url):
        videoid = url.split("show_",1)
        videoid = videoid[1].split("_external",1)
        date = url.split("mp4:",1)
        date2 = date[1].split("/",1)
        return (date2[0] + "_" + videoid[0])

def urlandname (mainurl):
        rtmp = getrtmp(mainurl)
        filename = date(rtmp) + ".mp4"
        output = (rtmp,filename)
        return (output)

def urlmod(url):
        print(url)
        urlcounter = url.split("&i=",1)
        counter = int(urlcounter[1])
        counter = counter + 1
        previousvideoname = urlcounter[0] + "&i="
        return (previousvideoname + str(counter))
                
def increment(startingurl, filename):
        oldurl = startingurl
        oldvideo = urlandname(startingurl)
        oldvideourl = oldvideo[0]
        oldname = oldvideo[1]
        newname = ''
        f=open(filename,"w")
        #f.write(oldvideourl + ", " + oldname + "\n")
        f.write("rtmpdump -r " + oldvideourl + " -o " + oldname + "\n")
        while True:
                newurl = urlmod(oldurl)
                newvideo = urlandname(newurl)
                newname = newvideo[1]
                newvideourl = newvideo[0]
                oldurl = newurl
                if oldname == newname:
                        f.close()
                        return ("All Links Extracted")
                else:
                        oldname = newvideo[1]
                        #f.write(newvideourl + ", " + newname + "\n")
                        f.write ("rtmpdump -r " + newvideourl + " -o " + newname + "\n")

def start():
        url = input('Please enter the first video url : ')
        filename = input('Please input the desired filename : ')
        print (url, filename)
        increment(url, filename)

start()
