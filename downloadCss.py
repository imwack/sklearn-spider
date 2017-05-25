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
            soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
            css = soup.find_all('link')
            js = soup.find_all('script')

            for c in css:
                curl = str(c['href']).strip()
                cpath = pre_url+curl[3:]
                print cpath
                try:
                    data = urllib2.urlopen(cpath).read()
                    path1 = "./document/" + curl[3:]
                    index1 = path1.rfind("/")
                    path1 = path1[0:index1]
                    if not os.path.exists(path1):
                        os.makedirs(path1)
                    fi = file("./document/"+curl[3:] , "wb")
                    fi.write(data)
                    fi.close()
                except :
                    print "error"
            for c in js:
                curl = str(c['src']).strip()
                cpath = pre_url+curl[3:]
                print cpath
                try:
                    data = urllib2.urlopen(cpath).read()
                    path1 = "./document/" + curl[3:]
                    index1 = path1.rfind("/")
                    path1 = path1[0:index1]
                    if not os.path.exists(path1):
                        os.makedirs(path1)
                    fi = file("./document/"+curl[3:] , "wb")
                    fi.write(data)
                    fi.close()
                except :
                    print "error"