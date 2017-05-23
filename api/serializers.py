from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import Match, Player, MatchPlayerResults


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['steam_id']
        extra_kwargs = {
            'player': {
                'validators': [UniqueValidator(queryset=Player.objects.all())],
            }
        }

    def validate(self, data):
        print "validate player", data
        return data

    def create(self, validated_data):
        print validated_data
        player_id = validated_data.pop('steam_id')
        player, created = Player.objects.get_or_create(steam_id=player_id)
        return player

    def update(self, instance, validated_data):
        print validated_data
        player_id = validated_data.pop('steam_id')
        player = Player.objects.get_or_create(steam_id=player_id)
        return player


class ResultsSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(many=False, read_only=False)

    class Meta:
        model = MatchPlayerResults
        fields = ('team', 'race', 'player')

    def validate(self, data):
        print "validate result", data
        return data

    def create(self, validated_data):
        print validated_data
        player_id = validated_data.pop('steam_id')
        player, created = Player.objects.get_or_create(steam_id=player_id)
        return player



class MatchSerializer(serializers.Serializer):

    @staticmethod
    def read(match):
        match_json = {}
        match_json['map'] = match.map
        match_json['date'] = match.date
        match_json['duration'] = match.duration
        match_json['players'] = []
        for matchplayer in match.matchplayerresults_set.all():
            result = MatchPlayerResults.objects.get(match=match, player=matchplayer.player)
            result_json ={}
            result_json['steam_id'] = result.player.steam_id
            result_json['race'] = result.race
            result_json['team'] = result.team
            match_json['players'].append(result_json)
        return match_json


    def create(self, validated_data):
        #players = validated_data.pop('players')
        match = Match.objects.create(**validated_data)
        return match

    def validate(self, data):
        print "validate match", data
        return data
