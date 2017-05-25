import json

from django.urls import reverse

from api.models import Match, Player, MatchPlayerResults
from api.serializers import MatchSerializer
import datetime
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.test import TestCase, Client


class MatchTestCase(TestCase):
    def setUp(self):
        p1 = Player.objects.create(steam_id=1)
        p2 = Player.objects.create(steam_id=2)

        match = Match.objects.create(map="turtlerock", winner=1, date=datetime.datetime.now(), duration=600)

        MatchPlayerResults.objects.create(player=p1, match=match, team=1, race="human")
        MatchPlayerResults.objects.create(player=p2, match=match, team=2, race="orc")

    '''def test_serializer(self):
        match = Match.objects.get()
        serializer = MatchSerializer.read(match)
        content = JSONRenderer().render(serializer)

        self.assertEqual(content, '{"date":"2017-05-25T12:43:01Z","map":"turtlerock","duration":600,"players":[{"steam_id":1,"race":"human","team":1},{"steam_id":2,"race":"orc","team":2}]}')
'''

class PlayerRaceTestCase(TestCase):
    def setUp(self):
        self.players = []
        for i in range(1,3):
            p = Player.objects.create(steam_id=i)
            self.players.append(p)

        match = Match.objects.create(map="turtlerock", winner=1, date=datetime.datetime.now(), duration=600)

        MatchPlayerResults.objects.create(player=self.players[0], match=match, team=1, race="human")
        MatchPlayerResults.objects.create(player=self.players[1], match=match, team=2, race="human")


    def test_get_player_race_list(self):
         client = Client()
         response = client.get('/api/players/human')
         data = json.loads(response.content)
         self.assertEqual(response.status_code, 200)
         # Win from player
         self.assertEqual(data[0][1],1)
         #Rate from player
         self.assertEqual(data[0][2],'100.00')


class MatchListTestCase(TestCase):

    def test_create_match(self):
        players = []
        for i in range(1,3):
            p = {"player": i, "team": i, "race": "orc"}
            players.append(p)
        client = Client()
        match = {"map": "turtlerock", "winner": 1, "duration": 600, "players": players}

        response = client.post('/api/matches', json.dumps(match), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(2, Player.objects.all().count())
        self.assertEqual(1, Match.objects.all().count())






