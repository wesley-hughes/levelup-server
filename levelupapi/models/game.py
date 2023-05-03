from django.db import models
from .game_type import GameType

class Game(models.Model):
    title = models.CharField(max_length=155)
    maker = models.CharField(max_length=155)
    number_of_players = models.IntegerField()
    skill_level = models.CharField(max_length=155)
    game_type = models.ForeignKey('GameType', on_delete=models.CASCADE, related_name='games')
    creator = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name='games_created')