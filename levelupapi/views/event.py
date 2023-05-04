"""View module for handling requests about game s"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event 

        Returns:
            Response -- JSON serialized event 
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        if "game" in request.query_params:
            game_id = request.query_params["game"]
            events = events.filter(game_id=game_id)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'number_of_players', 'skill_level', 'game_type', 'creator')
class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('id', 'full_name')
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    organizer = GamerSerializer(many=False)
    attendees = GamerSerializer(many=True, read_only=True)
    game = GameSerializer(many=False)
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time', 'attendees', 'game', 'organizer')