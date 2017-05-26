# -*- coding: utf-8 -*-
import urlparse
import urllib2
from bs4 import BeautifulSoup
import re
import csv
import __main__

url = ""
IngUrls = [url]
EdUrls = [url]
hrefs = []

global hrefs

while len(IngUrls) > 0:
    try:
        #print IngUrls
        htmltext = urllib2.urlopen(IngUrls[0]).read()
    except:
        print 'except 1'
        #print IngUrls[0]
        pass

    soup = BeautifulSoup(htmltext, "lxml")
    IngUrls.pop(0)
    #print len(IngUrls)

class Crawle:

    def GetUrl(self):
        #### First get
        ayamamo.genre(soup)
        #print hrefs

        dup = ''
        lhref = url + hrefs[-1]
        #### != First get
        while url + hrefs[-1] != dup:
            try:
                dup = url + hrefs[-1]
                get_page = urllib2.urlopen(url + hrefs[-1]).read()
                get_soup = BeautifulSoup(get_page, 'lxml')
                ayamamo.genre(get_soup)
                print hrefs
            except:
                print 'except 2'
                pass

        ### While exits url
        while len(hrefs) > 0:
            try:
                htmtex = urllib2.urlopen(url + hrefs[0]).read()
                scr_soup = BeautifulSoup(htmtex, 'lxml')
                ayamamo.TitleMail(scr_soup)
                print len(hrefs)
                hrefs.pop(0)
            except:
                hrefs.pop(0)
                print 'except 3'
                pass

    #### Get mail and title
    def TitleMail(self, x):
        self.x = x
        for MailTag in self.x.findAll("a", class_='emailLink'):
            ParentMail = MailTag.parent.parent
            pattern = "'[a-zA-Z0-9].*@[a-zA-Z0-9].*'"
            Mail = re.search(pattern, MailTag['onclick']).group(0)
            if Mail is not None:
                for TitleTag in ParentMail.findAll("a", class_='blueText'):
                    print TitleTag.string
                    print Mail
                    #### bs4.element.NavigableString to str
                    Titl = TitleTag.string.encode('utf-8')
                    ayamamo.Output(Titl, Mail)
            else:
                pass

        f.close()

    #### Output csv
    def Output(self, x, y):
        self.x = x
        self.y = y
        f = open('/Users/[]/Desktop/crawler/ITP/test.csv', 'a')# a 上書き, w 新規書き込み

        writer = csv.writer(f, lineterminator='\n')
        csvlist = []
        csvlist.append(self.x)
        csvlist.append(self.y)

        writer.writerow(csvlist)

        #f.close()
        global f

    #### Get after variable url vlaues
    def genre(self, x):
        self.x = x
        for n in self.x.findAll("div", class_='bottomNav'):
            for h in n.findAll("a", href=re.compile('/genre_dir/.*')):
                href = h.get('href')
                pattern = "(.[a-zA-Z0-9\_]+/){2}"
                spurl = href.replace(re.search(pattern, href).group(0), '')
                hrefs.append(spurl)
            __main__.hrefs = sorted(set(hrefs), key=hrefs.index)


ayamamo = Crawle()
ayamamo.TitleMail(soup)
ayamamo.GetUrl()
