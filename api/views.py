from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Match, Player, MatchPlayerResults
from api.serializers import MatchSerializer, PlayerSerializer
from datetime import datetime
from random import randint

@api_view(['POST'])
def create_random_matches(request):
    """
    Creates a player
    """
    if request.method == 'POST':
        match_data = request.data
        cant = match_data.pop('cant')
        for x in range(0,cant):
            create_random_match()
        return Response({"Created {} matches".format(cant, 1)}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def match_list(request):
    """
    List all matches, or create a new match.
    """
    if request.method == 'GET':
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        match_data = request.data
        results = match_data.pop('players')
        match = Match.objects.create(**match_data)
        for result in results:
            player, created = Player.objects.get_or_create(steam_id=result['player'])
            result_o = MatchPlayerResults.objects.create(player=player, match=match,
                                                        team=result['team'], race=result['race'])
            print result_o
        print match
        match.save()
        return Response({"Created"}, status=status.HTTP_201_CREATED)
        #serializer = MatchSerializer(data=request.data)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def match_detail(request, pk):
    """
    Retrieve a match instance
    """
    try:
        snippet = Match.objects.get(pk=pk)
    except Match.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatchSerializer(snippet)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def player_list(request):
    """
    List all players
    """
    if request.method == 'GET':
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def player_detail(request, pk):
    """
    Retrieve a player instance
    """
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)


def create_random_match():
    cant_players = randint(1, 8)
    players = []
    teams = []
    maps = ['Echo Isles', 'Melting Valley', 'Road to Stratholme', 'Secret Valley', 'Terenas Stand', 'Tirisfal Glades',
            'Broken Shard', 'Centaur Grove', 'Lost Temple', 'Tidewater Glades', 'Turtle Rock', 'Twisted Meadows']
    races = ['orc', 'human', 'elf', 'undead', 'cuchuflito']
    map = maps[randint(0, maps.__len__()-1)]
    duration = randint(20, 320)
    match = Match.objects.create(map=map, winner=0, duration=duration)
    for i in range (0, cant_players):
        steam_id = randint(1, 80)
        while players.__contains__(steam_id):
            steam_id = randint(1, 80)
        players.append(steam_id)
        team = randint(1, 8)
        teams.append(team)
        race = races[randint(0, races.__len__()-1)]
        player, created = Player.objects.get_or_create(steam_id=steam_id)
        result_o = MatchPlayerResults.objects.create(player=player, match=match, team=team, race=race)
        result_o.save()
    winner = teams[randint(0, teams.__len__()-1)]
    match.winner = winner
    match.save()
