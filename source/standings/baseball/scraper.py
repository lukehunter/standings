import re
from BeautifulSoup import BeautifulSoup, NavigableString
#from urllib import urlopen

def printScores(soup, findAttrs):
    curTeam = soup.find(attrs=findAttrs)
    while(curTeam is not None):
        if (curTeam.b is not None and curTeam.b.a is not None):
            teamLink = curTeam.b.a['href']
            teamname = teamLink.strip()[-3:]
            print "%s" % (teamname),

            scoreTag = curTeam.findNext('span')
            if (scoreTag is not None and scoreTag.contents[0].isdigit()):
                score = scoreTag.contents[0].strip()
                print "%s" % (score),
            print ""
        curTeam = curTeam.findNext(attrs=findAttrs)

def getStandings(soup):
    results = []
    for tr in soup.findAll(attrs={'class' : re.compile('ysptblthbody1|ysprow1|ysprow2')}):
        firstCell = tr.findChildren('td')[0]
        if (firstCell is not None and firstCell.a is None):
            keys = tr.findChildren('td')
            rank = 1
        if (tr['class'] != 'ysptblthbody1'):
            cols = tr.findChildren('td')
            result = {}
            result['rank'] = rank
            for td in range(len(cols)):
                if (cols[td].a is not None):
                    result['team'] = cols[td].a['href'].strip()[-3:]
                else:
                    result[keys[td].contents[0].strip()] = cols[td].contents[0].strip()
            results.append(result)
            rank += 1
    return results
        

##todayScores = open('C:\projects\standings\source\sampledata\mlb-scoreboard.html','r').read()#urlopen('http://sports.yahoo.com/mlb/scoreboard').read()
##todayScoresSoup = BeautifulSoup(todayScores)
##findScoreAttrs = {'class' : re.compile('yspscores team')}
##
##printScores(todayScoresSoup, findScoreAttrs)
##
##print "\n*********************************\n"
##
##futureScores = open('c:\projects\standings\source\sampledata\mlb-scoreboard-future.html','r').read()
##futureScoresSoup = BeautifulSoup(futureScores)
##findMatchupsAttrs = {'class' : re.compile('yspscores')}
##
##printScores(futureScoresSoup, findMatchupsAttrs)
##
##print "\n*********************************\n"

standings = open('c:\projects\standings\source\sampledata\mlb-standings.html','r').read()
standingsSoup = BeautifulSoup(standings, convertEntities=BeautifulSoup.HTML_ENTITIES)
standingsDictArr = getStandings(standingsSoup)
for standingsDict in standingsDictArr:
    for key in standingsDict.keys():
        print "%s:%s " % (key, standingsDict[key]),
    print ''

