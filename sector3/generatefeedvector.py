import os
import re
import feedparser

def get_words(html):
    # replace all html tags
    txt = re.sub(r'<[^>]+>', '', html)
    res = re.split(r'[^a-z^A-Z]+', txt)

    return [word for word in res if word != '']

def get_wordcount(url):
    d = feedparser.parse(url)
    wc = {}

    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description

html = ''\
'<?xml version="1.0" encoding="utf-8"?>'\
'<feed xmlns="http://www.w3.org/2005/Atom">'\
'<title type="text">博客园_mrbean</title>'\
'<subtitle type="text">**********************</subtitle>'\
'<id>uuid:32303acf-fb5f-4538-a6ba-7a1ac4fd7a58;id=8434</id>'\
    '<updated>2014-05-14T15:13:36Z</updated>'\
    '<author>'\
        '<name>mrbean</name>'\
        '<uri>http://www.cnblogs.com/MrLJC/</uri>'\
    '</author>'\
    '<generator>feed.cnblogs.com</generator>'\
    '<entry>'\
        '<id>http://www.cnblogs.com/MrLJC/p/3715783.html</id>'\
        '<title type="text">用python读写excel（xlrd、xlwt） - mrbean</title>'\
        '<summary type="text">最近需要从多个excel表里面用各种方式整...</summary>'\
        '<published>2014-05-08T16:25:00Z</published>'\
        '<updated>2014-05-08T16:25:00Z</updated>'\
        '<author>'\
            '<name>mrbean</name>'\
            '<uri>http://www.cnblogs.com/MrLJC/</uri>'\
        '</author>'\
        '<link rel="alternate" href="http://www.cnblogs.com/MrLJC/p/3715783.html" />'\
        '<link rel="alternate" type="text/html" href="http://www.cnblogs.com/MrLJC/p/3715783.html" />'\
        '<content type="html">最近需要从多个excel表里面用各种方式整理一些数据，虽然说原来用过java做这类事情，但是由于最近在学python，所以当然就决定用python尝试一下了。发现python果然简洁很多。这里简单记录一下。（由于是用到什么学什么，所以不算太深入，高手勿喷，欢迎指导）一、读excel表读excel要用...<img src="http://counter.cnblogs.com/blog/rss/3715783" width="1" height="1" alt=""/><br/><p>本文链接：<a href="http://www.cnblogs.com/MrLJC/p/3715783.html" target="_blank">用python读写excel（xlrd、xlwt）</a>，转载请注明。</p></content>'\
    '</entry>'\
'</feed>'

if __name__ == '__main__':
    print(get_words(html))

