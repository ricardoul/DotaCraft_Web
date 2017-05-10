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

    def create(self, validated_data):
        #players = validated_data.pop('players')
        match = Match.objects.create(**validated_data)

        return match

    def validate(self, data):
        print "validate match", data
        return data
