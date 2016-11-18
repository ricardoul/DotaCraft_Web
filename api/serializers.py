from rest_framework import serializers
from api.models import Match


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('steam_id', 'team', 'race', 'duration', 'players')


class MatchSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Match
        fields = ('map', 'winner', 'date', 'duration', 'players')


