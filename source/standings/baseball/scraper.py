from BeautifulSoup import BeautifulSoup, NavigableString
#from urllib import urlopen

def getText(tags):
    for tag in tags:
        if tag.__class__ == NavigableString:
            return tag,
        else:
            return getText(tag)

def printTeams(tag, findAttrs):
    curTeam = tag
    scores = []
    newline = 0
    while(curTeam is not None):
        if (curTeam.b is not None and curTeam.b.a is not None):
            teamText = curTeam.b.a.contents[0]
            #print "%s - %s" % (type(teamText), teamText)
            teamname = teamText.strip()

            print "%s" % (teamname)
            if (newline % 2 == 1):
                print ("\n")
            newline += 1
        curTeam = curTeam.findNext(attrs=findAttrs)

def printScores(tag, findAttrs):
    curTeam = tag
    scores = []
    newline = 0
    while(curTeam is not None):
        if (curTeam.b is not None and curTeam.b.a is not None):
            teamText = curTeam.b.a.contents[0]
            #print "%s - %s" % (type(teamText), teamText)
            teamname = teamText.strip()

            scoreTag = curTeam.findNext('span')
            if (scoreTag is not None):
                score = scoreTag.contents[0]
            print "%s: %s" % (teamname, score)
            scores.append((teamname, score))
        curTeam = curTeam.findNext(attrs=findAttrs)
        if (newline % 2 == 1):
            print ("\n")
        newline += 1

html_data = open('C:\projects\standings\source\sampledata\mlb-scoreboard.html','r').read()#urlopen('http://sports.yahoo.com/mlb/scoreboard').read()
soup = BeautifulSoup(html_data)

findAttrs = {'class' : re.compile('yspscores team')}

firstTeam = soup.find(attrs=findAttrs)
if (firstTeam is not None):
    printScores(firstTeam, findAttrs)

print "\n\n*********************************\n\n"

html_data2 = open('c:\projects\standings\source\sampledata\mlb-scoreboard-future.html','r').read()
soup2 = BeautifulSoup(html_data2)
findAttrs2 = {'class' : re.compile('yspscores')}
teamlinkAttrs = {'href' : re.compile('teams')}

firstTeam2 = soup2.find(attrs=findAttrs2)
if (firstTeam2 is not None):
    printTeams(firstTeam2, findAttrs2)

