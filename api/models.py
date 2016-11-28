from django.db import models


class Player(models.Model):
    steam_id = models.IntegerField(primary_key=True)

    def __unicode__(self):
        return 'Player {}'.format(self.steam_id)


class Match(models.Model):
    map = models.CharField(max_length=30)
    winner = models.IntegerField()
    date = models.DateField()
    duration = models.IntegerField()
    players = models.ManyToManyField(Player, through='MatchPlayerResults')

    def __unicode__(self):
        results = ''
        players = self.players.all()

        for player in players.iterator():
            player_result = MatchPlayerResults.objects.filter(match_id=self.id, player__steam_id=player.steam_id)
            results += '\tPlayer {}: {}\n'.format(player.steam_id, player_result)

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
