from rest_framework import serializers
from api.models import Match, Player, MatchPlayerResults
from datetime import datetime


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['steam_id']


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchPlayerResults
        fields = ('player', 'team', 'race')


class MatchSerializer(serializers.ModelSerializer):
    players = ResultsSerializer(many=True)

    class Meta:
        model = Match
        fields = ('map', 'winner', 'date', 'duration', 'players')

    def create(self, validated_data):
        map = validated_data.pop('map')
        winner = validated_data.pop('winner')
        duration = validated_data.pop('duration')
        date = datetime.now().time()
        match = Match.objects.create(map=map, winner=winner, duration=duration, date=date)

        results = validated_data.pop('players')
        for result in results:
            player = Player.objects.get_or_create(name=result['player'])
            result = ResultsSerializer(result)
            match.players.add(player)
        return match
