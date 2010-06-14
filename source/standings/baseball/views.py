from django.shortcuts import render_to_response
from standings.baseball.models import Team, League, Division

def index(request):
   team_list = Team.objects.all()
   return render_to_response('baseball/index.html', {'team_list': team_list})