from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Match, Player, MatchPlayerResults
from api.serializers import MatchSerializer, PlayerSerializer
from datetime import datetime

@api_view(['POST'])
def create_player(request):
    """
    Creates a player
    """
    if request.method == 'POST':
        # Player.objects.update_or_create(pk=request.data['steam_id'], defaults=request.data)
        # return HttpResponse("Yaay!")
        serializer = PlayerSerializer(data=request.data, validators=[])
        serializer.validators = []
        a = serializer.is_valid()
        if a:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
