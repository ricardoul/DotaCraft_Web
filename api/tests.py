from api.models import Match, Player, MatchPlayerResults
from api.serializers import MatchSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.test import TestCase


class MatchTestCase(TestCase):
    def setUp(self):
        p1 = Player(steam_id=1)
        p1.save()
        p2 = Player(steam_id=1)
        p2.save()
        players = [p1, p2]

        match = Match.objects.create(map="turtlerock", winner="1", duration="600", players=players)

        results_p1 = Player.objects.create(player=1, match=match.id, team=1, race="human")
        results_p2 = Player.objects.create(player=2, match=match.id, team=2, race="orc")


def test_serializer(self):
        """"""
        match = Match.objects.get()
        serializer = MatchSerializer(match)
        serializer.data
        #self.assertEqual()
