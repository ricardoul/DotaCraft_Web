from django.db import models
from django.db.models import Count
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver


class Player(models.Model):
    steam_id = models.IntegerField(primary_key=True)
    wins = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    solo_wins = models.IntegerField(default=0)
    solo_matches = models.IntegerField(default=0)


    def __unicode__(self):
        return 'Player {}'.format(self.steam_id)

    def get_matches(self, **kwargs):
        return MatchPlayerResults.objects.filter(player=self, **kwargs).select_related().order_by('-match__date')

    def get_solo_matches(self):
        solo_pks = [o.pk for o in self.get_matches() if o.is_solo()]
        return MatchPlayerResults.objects.filter(pk__in=solo_pks).select_related().order_by('-match__date')

    def get_race_matches(self,race):
        return MatchPlayerResults.objects.filter(player=self, race=race).select_related().order_by('-match_date')


    def winrate(self):
        if self.matches == 0:
            return "{0:.2f}".format(round(0, 2))
        rate = (self.wins*1.0/self.matches*1.0)*100.0
        return "{0:.2f}".format(round(rate, 2))

    def c_wins(self):
        return self.get_matches().filter(match__winner=F('team')).count()

    def c_matches(self):
        return self.get_matches().count()

    def c_matches_race(self, race):
       return self.get_race_matches(race).count()

    def c_wins_race(self,race):
        return self.get_race_matches(race).filter(match__winner=F('team')).count()

    def f_race_winrate(self,race):
        if self.c_matches_race(race) == 0:
            return "{0:.2f}".format(round(0, 2))
        rate = (self.c_wins_race(race)*1.0/self.c_matches_race(race)*1.0)*100.0
        return "{0:.2f}".format(round(rate, 2))

    def f_winrate(self):
        if self.c_matches() == 0:
            return "{0:.2f}".format(round(0, 2))
        rate = (self.c_wins()*1.0/self.c_matches()*1.0)*100.0
        return "{0:.2f}".format(round(rate, 2))

    def favorite_race(self):
        if self.matches == 0:
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

    def c_solo_wins(self):
        return self.get_solo_matches().filter(match__winner=F('team')).count()

    def f_solo_winrate(self):
        if self.c_solo_matches() == 0:
            return "{0:.2f}".format(round(0, 2))
        rate = (self.c_solo_wins()*1.0/self.c_solo_matches()*1.0)*100.0
        return "{0:.2f}".format(round(rate, 2))

    def solo_winrate(self):
        if self.solo_matches == 0:
            return "{0:.2f}".format(round(0, 2))
        rate = (self.solo_wins*1.0/self.solo_matches*1.0)*100.0
        return "{0:.2f}".format(round(rate, 2))


class Match(models.Model):
    map = models.CharField(max_length=30)
    winner = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
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

