from flask import Blueprint, request, jsonify, current_app
from bson.json_util import dumps
from .models import Player, Configuration

main = Blueprint('main', __name__)

@main.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@main.route('/configurations', methods=['POST'])
def create_or_update_configuration():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    player_model = Player(current_app.db)
    config_model = Configuration(current_app.db)
    
    player = player_model.get(data['player'])
    if not player:
        return jsonify({"error": "Player not found"}), 404
    
    config = config_model.create_or_update(
        nb_players=data.get('nb_players'),
        nb_partie=data.get('nb_partie'),
        nb_dices=data.get('nb_dices'),
        timer=data.get('timer'),
        player_id=data['player']
    )
    return jsonify(config), 201

@main.route('/configurations/<config_id>', methods=['GET'])
def get_configuration(config_id):
    config_model = Configuration(current_app.db)
    config = config_model.get(config_id)
    if not config:
        return jsonify({"error": "Configuration not found"}), 404
    return jsonify(config), 200

@main.route('/configurations/player/<player_id>', methods=['GET'])
def get_configuration_by_player(player_id):
    config_model = Configuration(current_app.db)
    config = config_model.get_by_player(player_id)
    if not config:
        return jsonify({"error": "Configuration not found"}), 404
    return jsonify(config), 200

@main.route('/configurations/<config_id>', methods=['PUT'])
def update_configuration(config_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    config_model = Configuration(current_app.db)
    config = config_model.get(config_id)
    if not config:
        return jsonify({"error": "Configuration not found"}), 404
    
    config_model.update(config_id, data)
    updated_config = config_model.get(config_id)
    return jsonify(updated_config), 200

@main.route('/configurations/<config_id>', methods=['DELETE'])
def delete_configuration(config_id):
    config_model = Configuration(current_app.db)
    config = config_model.get(config_id)
    if not config:
        return jsonify({"error": "Configuration not found"}), 404
    
    config_model.delete(config_id)
    return jsonify({"message": "Configuration deleted"}), 200
