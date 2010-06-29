from django.shortcuts import render_to_response
from standings.baseball.baseballmodel import Team, League, Division
from standings.baseball.scraper import getContests, getStandings, printDict, printDictArr
from itertools import *

def index(request):
   team_list = Team.objects.all()
   divisionmap = dict((k,list(v)) for k,v in groupby(team_list, key=lambda team: team.division.league.name + " " + team.division.name))
   return render_to_response('baseball/index.html', {'divisionmap': divisionmap})
   
def scraper(request, profile):
   return render_to_response('baseball/scraper.html', {'profile': profile})