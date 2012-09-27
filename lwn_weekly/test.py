from calibre.ebooks.BeautifulSoup import BeautifulSoup
import re
import sys
from tempfile import mkstemp
import hashlib

from pprint import pprint as pp
from pprint import pformat

soup = BeautifulSoup(open('lwn.html'))

#print soup.prettify()

curr = soup.body

articles = {}
ans = []

section = 'Front Page'
subsection = None

while True:
    curr = curr.findNext(attrs = {'class': ['SummaryHL', 'Cat1HL', 'Cat2HL'] })

    if curr == None:
        break

    text = curr.contents[0].string

    if 'Cat2HL' in curr.attrMap['class']:
        subsection = text

    elif 'Cat1HL' in curr.attrMap['class']:
        section = text
        subsection = None

    elif 'SummaryHL' in curr.attrMap['class']:
        article_title = text
        print 'curr is "%s"' % str(curr)

        if subsection:
            section_title = "%s: %s" % (section, subsection)
        else:
            section_title = section
        
        # Most articles have anchors in their titles, *except* the security vulnerabilities
        article_anchor = curr.findNext(text=re.compile('^[Cc]omments( [(]\w+? posted[)]|: \w+)$'))

        if article_anchor:
            article_anchor = article_anchor.parent

        print 'Looking for article_anchor "%s"' % str(article_anchor)
        print 'For article "%s"' % article_title
        #curr = curr.findNext(attrs = {'class': ['SummaryHL', 'Cat1HL', 'Cat2HL'] })
        article_body = []
        #nextelem = curr.findNext(name='p')
        nextelem = curr.nextSibling
#        while nextelem != None \
#                and nextelem != article_anchor \
#                and not str(article_anchor) in str(nextelem):
        while True:
            print 'Examining nextelem: """%s"""' % str(nextelem)
            
            if nextelem == None:
                print 'Breaking because nextelem == None'
                break
            elif nextelem == article_anchor:
                print 'Breaking because nextelem == article_anchor'
                break
            elif str(article_anchor) in str(nextelem):
                print 'Breaking because str(article_anchor) in nextelem'
                break
            article_body.append(str(nextelem))
            nextelem = nextelem.nextSibling

        #article_body = ''.join(article_body)
        #print 'Article body was "%d" lines' % (len(article_body),)

        if len(article_body) < 2:
            article_body = []
            nextelem = curr.findNext(name='p')
    #        while nextelem != None \
    #                and nextelem != article_anchor \
    #                and not str(article_anchor) in str(nextelem):
            while True:
                print 'Examining nextelem: """%s"""' % str(nextelem)
                
                if nextelem == None:
                    print 'Breaking because nextelem == None'
                    break
                elif nextelem == article_anchor:
                    print 'Breaking because nextelem == article_anchor'
                    break
                elif str(article_anchor) in str(nextelem):
                    print 'Breaking because str(article_anchor) in nextelem'
                    break
                article_body.append(str(nextelem))
                nextelem = nextelem.nextSibling

#        (artfile, artfilename) = mkstemp(suffix='.html', prefix='lwn-', dir='/tmp/lwn')
        md5 = hashlib.md5()
        md5.update(article_title)
        artfilename = '/tmp/lwn/lwn-' + str(md5.hexdigest()[:12]) + '.html'
        print ">>> Writing to %s" % artfilename

        artfile = open(artfilename, 'w')
        #artfile.writelines(['<h1>%s</h1><h2>%s</h2>' % (section_title, article_title)])
        artfile.writelines(article_body)
        #artfile.writelines(['<h3>Chunks: %d</h3>' % len(article_body)])
        artfile.close()

        article_url = 'file://' + artfilename

        if section_title not in articles:
            articles[section_title] = []

        articles[section_title].append({
                'url': article_url,
                'title': article_title,
                'article_anchor': article_anchor,
                'last_nextelem': nextelem,
                'description': '', 'content': '', 'date': '',
            })

    else:
        print "something bad happened; should not be able to reach this"


ans = [(section, articles[section]) for section in articles]

#pp(ans)
