#from django.db import models
from djongo import models
from bson import ObjectId

class Players(models.Model):
    _id = models.ObjectIdField(default=ObjectId, primary_key=True, editable=False)
    #mongo_id = models.CharField(max_length=24, unique=True)  # Pour stocker l'ObjectId de MongoDB
    username = models.CharField(max_length=255, null=True, blank=True, default=None)
    last_connexion = models.DateTimeField(null=True, blank=True, default=None)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Player {self.username}, last seen on {self.last_connexion}."

# Create your models here.
class Settings(models.Model):
    #player = models.ForeignKey(Players, on_delete=models.CASCADE)
    player = models.EmbeddedField(
        model_container=Players
    )
    nb_players = models.IntegerField(null=True, default=None)
    nb_partie = models.IntegerField(null=True, default=None)
    nb_dices = models.IntegerField(null=True, default=None)
    timer = models.IntegerField(null=True, default=None)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game with {self.nb_players} players, {self.nb_partie} parties, {self.nb_dices} dices, and a timer of {self.timer} seconds."
    
    def to_dict(self):
        return {
            #"id": self.id,
            "player": self.player["username"],
            "nb_players": self.nb_players,
            "nb_partie": self.nb_partie,
            "nb_dices": self.nb_dices,
            "timer": self.timer,
        }
