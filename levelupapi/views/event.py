"""View module for handling requests about game s"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game
from django.db.models import Q
from rest_framework.decorators import action
from django.db.models import Count
from django.core.exceptions import ValidationError




class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event 

        Returns:
            Response -- JSON serialized event 
        """
        event = Event.objects.annotate(attendees_count=Count('attendees')).get(pk=pk)
        # event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.annotate(
            attendees_count=Count('attendees'),
            joined=Count(
                'attendees',
                filter=Q(attendees=gamer)
            )
)
        if "game" in request.query_params:
            game_id = request.query_params["game"]
            events = events.filter(game_id=game_id)
                # Set the `joined` property on every event 
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        game = Game.objects.get(pk=request.data["game"])
        event.game = game

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer left'}, status=status.HTTP_204_NO_CONTENT)
    

        
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'number_of_players', 'skill_level', 'game_type', 'creator')
class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('id', 'full_name')
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'game', 'organizer', 'description', 'date', 'time']
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    attendees_count = serializers.IntegerField(default=None)
    organizer = GamerSerializer(many=False)
    attendees = GamerSerializer(many=True, read_only=True)
    game = GameSerializer(many=False)
    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer',
          'description', 'date', 'time', 'attendees',
          'joined', 'attendees_count')