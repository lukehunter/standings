import re
from BeautifulSoup import BeautifulSoup, NavigableString
from urllib import FancyURLopener
from datetime import datetime

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6'

# returns dictionary with keys: hometeam, homescore, awayteam, awayscore,
# start_time. if game hasn't started scores will be empty and start_time
# will be full. otherwise start_time will be empty and scores will be full.
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

# returns dictionary with keys corresponding to headers from standings page as well as entries
# 'conference' and 'div'
def getStandings(soup):
    results = []
    for tr in soup.findAll(attrs={'class' : re.compile('yspsctbg|ysptblthbody1|ysprow1|ysprow2')}):
        firstCell = tr.findChildren('td')[0]
        if (firstCell is not None):
            if (firstCell.get('class') == 'yspdetailttl'):
                keys = tr.findChildren('td')
                rank = 1
                division = tr.td.contents[0].strip()
            else:
                if (firstCell.get('class') == 'ysptblhdr'):
                    conference = tr.td.contents[0].strip()
        if (tr.get('class') != 'ysptblthbody1' and tr.get('class') != 'yspsctbg'):
            cols = tr.findChildren('td')
            result = {}
            result['rank'] = rank
            result['div'] = division
            result['conference'] = conference
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

def soupify(url):
    myopener = MyOpener()
    html = myopener.open(url).read()
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
    return soup

def getScoreboard(urlParams=""):
    url = 'http://sports.yahoo.com/mlb/scoreboard%s' % urlParams
    scoreboardSoup = soupify(url)
    scoreboardDictArr = getContests(scoreboardSoup)
    return scoreboardDictArr

def updateTodayScores():
    result = []

    for d in getScoreboard():
        if (d.get('homescore')):
            print "Found score: %s-%s %s, updating" % (d['homescore'], d['awayscore'], d['hometeam'])
            result.append(d)

    return result

def updateScheduledContests(date):
    result = []

    for d in getScoreboard(urlArgFromDate(date)):
        if (not d.get('homescore')):
            print "Found scheduled game: %s@%s %s/%s %s" % (d['awayteam'], d['hometeam'], date.month, date.day, d['start_time'])
            result.append(d)

    return result

def updateStandings():
    url = 'http://sports.yahoo.com/mlb/standings'
    standingsSoup = soupify(url)
    standingsDictArr = getStandings(standingsSoup)

    print "AL West"
    printDivision(standingsDictArr, "American League", "West")

def printDivision(standings, conference, division):
    for d in standings:
        if (d['conference'] == conference and d['div'] == division):
            print "%s. %s" % (d['rank'], d['team'])

def urlArgFromDate(date):
    return "?d=%d-%02d-%02d" % (date.year, date.month, date.day)

updateTodayScores()
updateScheduledContests(datetime(2010, 7, 30))
updateStandings()
