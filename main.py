#coding=utf-8
import urllib2
import re
import os
from bs4 import BeautifulSoup

if __name__=="__main__":
    crawled_url = []
    pre_url = "http://scikit-learn.org/stable/"
    root_url = "user_guide.html"
    response = urllib2.urlopen(pre_url+root_url)
    html = response.read()
    f = open("./document/"+root_url, 'wb')
    f.write(html)
    f.close()
    crawled_url.append(root_url)

    # find all chapter
    chapter_urls = set()
    pattern = re.compile(r'''.+href="(.+)#.+''')
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    chapter = soup.find_all('a', class_="reference internal")
    for c in chapter:
        # print c['href']
        u = str(c['href']).split('#')[0]
        chapter_urls.add(u)

    for chapter_url in chapter_urls:
        response = urllib2.urlopen(pre_url + chapter_url)
        html = response.read()
        print chapter_url
        if len(chapter_url)>0:
            path = "./document/" + chapter_url
            index = path.rfind("/")
            path = path[0:index]
            if not os.path.exists(path):
                os.makedirs(path)
            f = open("./document/" + chapter_url, 'wb')
            f.write(html)
            f.close()
            crawled_url.append(chapter_url)

            #crawl image
            soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
            imgs = soup.find_all('img')
            for img in imgs:
                imgurl = str(img['src']).strip()
                imgpath = pre_url+imgurl[3:]
                print imgpath
                try:
                    data = urllib2.urlopen(imgpath).read()
                    path1 = "./document/" + imgurl[3:]
                    index1 = path1.rfind("/")
                    path1 = path1[0:index1]
                    if not os.path.exists(path1):
                        os.makedirs(path1)
                    fi = file("./document/"+imgurl[3:] , "wb")
                    fi.write(data)
                    fi.close()
                except :
                    print "error"