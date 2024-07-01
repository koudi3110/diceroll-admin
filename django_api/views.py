from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_api.models import Settings, Players
#from django_api.serializers import SettingsSerializer
from rest_framework import status
from utils import get_db_handle
#from bson import ObjectId
#from django.utils import timezone


# Create your views here.
@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def view_settings(request, username):
    # GET method to retrieve settings for one player
    if request.method == "GET":
        db = get_db_handle("3icp", "localhost", "27017", "", "")
        playerCollection = db["django_api_players"]
        if not username:
            return Response(
                {"msg": "Missing username argument"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        player = playerCollection.find_one({"username": username})
        if player:
            settingCollection = db["django_api_settings"]
            setting = settingCollection.find_one({"player._id": player["_id"]})
            if setting:
                return Response(
                    {
                        "msg": f"Successfully retrieved setting for player {username}",
                        "data": setting["timer"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                default_setting = Settings.objects.create(
                    player=player, nb_players=2, nb_partie=4, nb_dices=3, timer=20
                )
                return Response(
                    {
                        "msg": f"Successfully created default setting for player {username}",
                        "data": default_setting.to_dict(),
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"msg": f"Unable to find any player with username {username}"},
                status=status.HTTP_404_NOT_FOUND,
            )

    # PUT method to update settings
    elif request.method == "PUT":
        required_fields = ["username", "nb_players", "nb_partie", "nb_dices", "timer"]
        for field in required_fields:
            if field not in request.data:
                return Response({"error": f"Field '{field}' is required in request data."}, status=status.HTTP_400_BAD_REQUEST)
            
        db = get_db_handle("3icp", "localhost", "27017", "", "")
        settingCollection = db["django_api_settings"]
        setting = settingCollection.update_one(
            {"player.username": request.data.get("username")},
            {
                "$set": {
                    "nb_players": request.data.get("nb_players"),
                    "nb_partie": request.data.get("nb_partie"),
                    "nb_dices": request.data.get("nb_dices"),
                    "timer": request.data.get("timer"),
                }
            },
        )
        return Response(
            {"msg": "Settings updated successfully"},
            status=status.HTTP_200_OK,
        )

    return Response(
        {"msg": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
