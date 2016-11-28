from rest_framework import serializers
from api.models import Match, Player


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('steam_id', )


class MatchSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Match
        fields = ('map', 'winner', 'date', 'duration', 'players')
