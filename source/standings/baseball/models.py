from django.db import models

class League(models.Model):
   name = models.CharField(max_length=64)
   def __unicode__(self):
      return self.name
   
class Division(models.Model):
   name = models.CharField(max_length=64)
   league = models.ForeignKey(League)
   def __unicode__(self):
      return self.league.name + " " + self.name
   
class Team(models.Model):
   name = models.CharField(max_length=64)
   city = models.CharField(max_length=64)
   abbrev = models.CharField(max_length=3)
   streak = models.CharField(max_length=10)
   wins = models.IntegerField()
   losses = models.IntegerField()
   score = models.IntegerField()
   opponent_score = models.IntegerField()
   opponent_abbrev = models.CharField(max_length=3)
   next_game = models.DateTimeField('next game')
   division = models.ForeignKey(Division)
   def __unicode__(self):
      return self.abbrev