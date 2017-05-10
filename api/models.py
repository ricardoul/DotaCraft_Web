from django.db import models
from django.db.models import Count
from django.db.models import F


class Player(models.Model):
    steam_id = models.IntegerField(primary_key=True)

    def __unicode__(self):
        return 'Player {}'.format(self.steam_id)

    def get_matches(self):
        return MatchPlayerResults.objects.filter(player=self)

    def get_solo_matches(self):
        solo_pks = [o.pk for o in self.get_matches() if o.is_solo()]
        return MatchPlayerResults.objects.filter(pk__in=solo_pks)

    def wins(self):
        return self.get_matches().filter(match__winner=F('team')).count()

    def c_matches(self):
        return self.get_matches().count()

    def winrate(self):
        if self.c_matches() == 0:
            return "{0:.2f}".format(round(0, 2))
        rate = (self.wins()*1.0/self.c_matches()*1.0)*100.0
        return "{0:.2f}".format(round(rate, 2)) #cast to float somehow

    def favorite_race(self):
        if self.c_matches() == 0:
            return 'none'
        fav = self.get_matches().values('race').annotate(count=Count('race')).latest('count')
        return fav['race']

    def favorite_solo_race(self):
        if self.c_solo_matches() == 0:
            return 'none'
        fav = self.get_solo_matches().values('race').annotate(count=Count('race')).latest('count')
        return fav['race']

    def c_solo_matches(self):
        return self.get_solo_matches().count()

    def solo_wins(self):
        return self.get_solo_matches().filter(match__winner=F('team')).count()

    def solo_winrate(self):
        if self.c_solo_matches() == 0:
            return "{0:.2f}".format(round(0, 2))
        rate = (self.solo_wins()*1.0/self.c_solo_matches()*1.0)*100.0
        return "{0:.2f}".format(round(rate, 2)) #cast to float somehow


class Match(models.Model):
    map = models.CharField(max_length=30)
    winner = models.IntegerField()
    date = models.DateField(auto_now=True)
    duration = models.IntegerField()
    players = models.ManyToManyField(Player, through='MatchPlayerResults')

    def __unicode__(self):
        results = ''
        players = self.players.all()

        for player in players.iterator():
            player_result = MatchPlayerResults.objects.get(match_id=self.id, player__steam_id=player.steam_id)
            results += '\t{}\n'.format(player_result)

        return '[Match {}] Map: {} | Duration: {} | Winner: Team {}\nResults:\n{}'.\
            format(self.id, self.map, self.duration, self.winner, results)


class MatchPlayerResults(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.IntegerField()
    race = models.CharField(max_length=10)

    def __unicode__(self):
        win = self.team == self.match.winner
        return '[Match {} Player {}] Race: {} | Team: {} | Victory: {}'.\
            format(self.match.id, self.player.steam_id, self.race, self.team, win)

    def is_solo(self):
        return MatchPlayerResults.objects.filter(match=self.match, team=self.team).count() == 1
