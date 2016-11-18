from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Match
from api.serializers import MatchSerializer


@api_view(['GET', 'POST'])
def match_list(request):
    """
    List all matches, or create a new match.
    """
    if request.method == 'GET':
        snippets = Match.objects.all()
        serializer = MatchSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
