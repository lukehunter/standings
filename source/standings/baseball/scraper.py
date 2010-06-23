import re
from BeautifulSoup import BeautifulSoup, NavigableString

def getContests(soup):
    results = []
    result = {}
    timeRe = re.compile(r"^[0-9]+:[0-9]{2}.*")
    homeOrAway = "away"
    for td in soup.findAll(attrs={'class' : re.compile('yspscores')}):
        if (td.b is not None and td.b.a is not None):
            result[homeOrAway + "team"] = td.b.a['href'].strip()[-3:]
            for span in td.findNext('span'):
                if span.isdigit():
                    result[homeOrAway + "score"] = span
                    break
                else:
                    if (timeRe.match(span)):
                        result["start_time"] = span
            if (homeOrAway == "away"):
                homeOrAway = "home"
            else:
                homeOrAway = "away"
                results.append(result)
                result = {}
    return results

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

def printDict(d):
    for key in d.keys():
        print "%s:%s " % (key, d[key]),

def printDictArr(da):
    for d in da:
        printDict(d)
        print ''
        

todayScores = open('C:\projects\standings\source\sampledata\mlb-scoreboard.html','r').read()#urlopen('http://sports.yahoo.com/mlb/scoreboard').read()
todayScoresSoup = BeautifulSoup(todayScores, convertEntities=BeautifulSoup.HTML_ENTITIES)
todayScoresDictArr = getContests(todayScoresSoup)
printDictArr(todayScoresDictArr)

print "\n*********************************\n"

futureScores = open('c:\projects\standings\source\sampledata\mlb-scoreboard-future.html','r').read()
futureScoresSoup = BeautifulSoup(futureScores, convertEntities=BeautifulSoup.HTML_ENTITIES)
futureScoresDictArr = getContests(futureScoresSoup)
printDictArr(futureScoresDictArr)
##
##print "\n*********************************\n"
##
##standings = open('c:\projects\standings\source\sampledata\mlb-standings.html','r').read()
##standingsSoup = BeautifulSoup(standings, convertEntities=BeautifulSoup.HTML_ENTITIES)
##standingsDictArr = getStandings(standingsSoup)
##printDictArr(standingsDictArr)


    

