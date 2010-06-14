from django.db import models

class League(models.Model):
   name = models.CharField(max_length=64)
   def __unicode__(self):
      return self.name
   
class Division(models.Model):
   name = models.CharField(max_length=64)
   league = models.ForeignKey(League)
   def tostring(self):
      return self.league.name + " " + self.name
   def __unicode__(self):
      return self.tostring()
   
class Team(models.Model):
   name = models.CharField(max_length=64)
   city = models.CharField(max_length=64)
   abbrev = models.CharField(max_length=3)
   streak = models.CharField(max_length=10, blank=True, null=True)
   wins = models.IntegerField(blank=True, null=True)
   losses = models.IntegerField(blank=True, null=True)
   score = models.IntegerField(blank=True, null=True)
   opponent_score = models.IntegerField(blank=True, null=True)
   opponent_abbrev = models.CharField(max_length=3, blank=True, null=True)
   next_game = models.DateTimeField('next game', blank=True, null=True)
   division = models.ForeignKey(Division)
   
   def win_pct(self):
      return float(self.wins) / (float(self.wins) + float(self.losses))
   def __unicode__(self):
      return self.abbrev