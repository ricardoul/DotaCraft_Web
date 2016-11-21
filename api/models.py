from django.db import models


class Player(models.Model):
    steam_id = models.IntegerField(primary_key=True)

    def __unicode__(self):
        return self.name


class Match(models.Model):
    map = models.CharField(max_length=30)
    winner = models.IntegerField()
    date = models.DateField()
    duration = models.IntegerField()
    players = models.ManyToManyField(Player, through='MatchPlayerResults')

    def __unicode__(self):
        return self.name


class MatchPlayerResults(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.IntegerField()
    race = models.CharField(max_length=10)
