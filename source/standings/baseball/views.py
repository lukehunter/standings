from django.shortcuts import render_to_response
from standings.baseball.models import Team, League, Division
from itertools import *

def index(request):
   team_list = Team.objects.all()
   divisionmap = dict((k,list(v)) for k,v in groupby(team_list, key=lambda team: team.division.league.name + " " + team.division.name))
   return render_to_response('baseball/index.html', {'divisionmap': divisionmap})