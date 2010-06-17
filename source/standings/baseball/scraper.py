from BeautifulSoup import BeautifulSoup, NavigableString
#from urllib import urlopen

def getText(tags):
    for tag in tags:
        if tag.__class__ == NavigableString:
            return tag,
        else:
            return getText(tag)

def printScores(soup, findAttrs):
    curTeam = soup.find(attrs=findAttrs)
    while(curTeam is not None):
        if (curTeam.b is not None and curTeam.b.a is not None):
            teamText = curTeam.b.a['href']
            teamname = teamText.strip()
            print "%s" % (teamname),

            scoreTag = curTeam.findNext('span')
            if (scoreTag is not None and scoreTag.contents[0].isdigit()):
                score = scoreTag.contents[0].strip()
                print "%s" % (score),
            print ""
        curTeam = curTeam.findNext(attrs=findAttrs)

html_data = open('C:\projects\standings\source\sampledata\mlb-scoreboard.html','r').read()#urlopen('http://sports.yahoo.com/mlb/scoreboard').read()
soup = BeautifulSoup(html_data)
findAttrs = {'class' : re.compile('yspscores team')}

printScores(soup, findAttrs)

print "\n*********************************\n"

html_data2 = open('c:\projects\standings\source\sampledata\mlb-scoreboard-future.html','r').read()
soup2 = BeautifulSoup(html_data2)
findAttrs2 = {'class' : re.compile('yspscores')}

printScores(soup2, findAttrs2)

