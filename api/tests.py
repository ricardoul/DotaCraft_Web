from api.models import Match, Player, MatchPlayerResults
from api.serializers import MatchSerializer
import datetime
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.test import TestCase


class MatchTestCase(TestCase):
    def setUp(self):
        p1 = Player.objects.create(steam_id=1)
        p2 = Player.objects.create(steam_id=2)

        match = Match.objects.create(map="turtlerock", winner=1, date=datetime.datetime.now(), duration=600)

        MatchPlayerResults.objects.create(player=p1, match=match, team=1, race="human")
        MatchPlayerResults.objects.create(player=p2, match=match, team=2, race="orc")

    def test_serializer(self):
        match = Match.objects.get()
        serializer = MatchSerializer(match)
        content = JSONRenderer().render(serializer.data)

        self.assertEqual(content, '{"map":"turtlerock","winner":1,"date":"2016-11-28","duration":600,"players":[{"steam_id":1},{"steam_id":2}]}')

