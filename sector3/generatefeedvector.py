import os
import re
import feedparser
import sys

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

def get_words(html):
    # replace all html tags
    txt = re.sub(r'<[^>]+>', '', html)
    res = re.split(r'[^a-z^A-Z]+', txt)

    return [word for word in res if word != '']

def get_wordcount(url):
    print(url)
    try:
        d = feedparser.parse(url)
        wc = {}
        for e in d.entries:
            if 'summary' in e:
                summary = e.summary
            else:
                summary = e.description

            words = get_words(e.title+" "+summary)
            for word in words:
                wc.setdefault(word, 0)
                wc[word]+=1
        print(">>> title : {}".format(d.feed.title))
        return d.feed.title, wc
    except Exception:
        return None, None

if __name__ == '__main__':
    feedlist_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'feedlist.txt')

    apcount = {}
    wordcounts = {}
    feedlist = open(feedlist_path, 'r').readlines()
    all_blogs = 0
    for feedurl in feedlist:
        feedurl = feedurl.strip()
        title, wc = get_wordcount(feedurl)
        if title is None:
            continue
        all_blogs += 1
        wordcounts[title] = wc
        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1
    print(">>> all word: ", len(apcount))
    wordlist = []
    for word, count in apcount.items():
        frac = float(count)/(all_blogs+1)
        if frac > 0.1 and frac < 0.5:
            wordlist.append(word)
    print(">>> ROI word: ", len(wordlist))
    out = open("blogdata.txt", 'w')
    out.write('Blog')
    for word in wordlist:
        out.write("\t%s" %word)
    out.write("\n")
    for blogname, words in wordcounts.items():
        out.write("{}".format(blogname))
        for w in wordlist:
            if w in words:
                out.write("\t{}".format(words[w]))
            else:
                out.write("\t0")
        out.write("\n")
    out.close()
