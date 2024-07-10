from datetime import datetime
from bson.objectid import ObjectId

class Player:
    def __init__(self, db):
        self.collection = db['players']

    def get(self, player_id):
        return self.collection.find_one({"_id": ObjectId(player_id)})

    def create(self, username, last_connexion):
        player = {
            "username": username,
            "last_connexion": last_connexion,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = self.collection.insert_one(player)
        created_player = self.collection.find_one({"_id": result.inserted_id})
        created_player["_id"] = str(created_player["_id"])
        return created_player

class Configuration:
    def __init__(self, db):
        self.collection = db['configurations']

    def create_or_update(self, nb_players, nb_partie, nb_dices, timer, player_id):
        # Vérifier si une configuration existe déjà pour ce joueur
        existing_config = self.collection.find_one({"player": ObjectId(player_id)})

        if existing_config:
            # Mettre à jour les champs de la configuration existante
            update_data = {
                "nb_players": nb_players,
                "nb_partie": nb_partie,
                "nb_dices": nb_dices,
                "timer": timer,
                "updated_at": datetime.utcnow()
            }
            self.collection.update_one(
                {"_id": existing_config["_id"]},
                {"$set": update_data}
            )
            # Récupérer et retourner la configuration mise à jour
            updated_config = self.collection.find_one({"_id": existing_config["_id"]})
            updated_config["_id"] = str(updated_config["_id"])
            updated_config["player"] = str(updated_config["player"])
            return updated_config
        else:
            # Créer une nouvelle configuration
            configuration = {
                "nb_players": nb_players,
                "nb_partie": nb_partie,
                "nb_dices": nb_dices,
                "timer": timer,
                "player": ObjectId(player_id),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            result = self.collection.insert_one(configuration)
            created_config = self.collection.find_one({"_id": result.inserted_id})
            created_config["_id"] = str(created_config["_id"])
            created_config["player"] = str(created_config["player"])
            return created_config

    def get(self, config_id):
        config = self.collection.find_one({"_id": ObjectId(config_id)})
        if config:
            config["_id"] = str(config["_id"])
            config["player"] = str(config["player"])
        return config

    def get_by_player(self, player_id):
        config = self.collection.find_one({"player": ObjectId(player_id)})
        if config:
            config["_id"] = str(config["_id"])
            config["player"] = str(config["player"])
        return config
    
    def update(self, config_id, data):
        data['updated_at'] = datetime.utcnow()
        self.collection.update_one(
            {"_id": ObjectId(config_id)},
            {"$set": data}
        )

    def delete(self, config_id):
        self.collection.delete_one({"_id": ObjectId(config_id)})
