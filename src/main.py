"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, favorite_characters, favorite_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/create/user', methods=['GET'])
def list_user():
    users = User(
    password = "123",
    email = "pruebaaa@example.com",
    is_active = True)

    db.session.add(users)
    db.session.commit()

    return jsonify("ok"), 200

@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    users = list(map(lambda user : user.serialize(), users))
    return jsonify(users), 200

@app.route('/create/favorites', methods=['GET'])
def create_user_favorites():
    user = User.query.get(1)
    character = Character.query.filter_by(name = "leia").first()
    user.favorite_characters.append(character)
    planet = Planet.query.filter_by(name = "Alderaan").first()
    user.favorite_planets.append(planet)
    db.session.add(user)
    db.session.commit()
    return jsonify("ok"), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    favorites = []
    for character in user.favorite_characters:
        favorites.append({"id": character.id,"name": character.name})
    for planet in user.favorite_planets:
        favorites.append({"id": planet.id,"name": planet.name})
    return jsonify(favorites), 200

@app.route('/create/characters', methods=['GET'])
def list_characters():
    characters = Character(
    name = "leia",
    height = "172",
    mass = "77",
    hair_color = "black",
    homeworld = "alderaan",
    eye_color = "brown",
    gender = "female")
    db.session.add(characters)
    db.session.commit()
    
    return jsonify(characters.serialize()), 200

@app.route('/people', methods=['GET'])
def get_character():
    characters = Character.query.all()
    characters = list(map(lambda character : character.serialize(), characters))
    return jsonify(characters), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200

@app.route('/people/<int:character_id>', methods=['GET'])
def get_one_person(character_id):
    character = Character.query.get(character_id)
    return jsonify(character.serialize()), 200

@app.route('/create/planets', methods=['GET'])
def list_planets():
    planets = Planet(
        diameter = "12500",
        population = "2000000000",
        climate = "temperate",
        terrain = "grasslands, mountains",
        surface_water = "40",
        name = "Alderaan"
    )
    db.session.add(planets)
    db.session.commit()
    
    return jsonify(planets.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    planet = Planet.query.get(planet_id)
    user = User.query.get(1)
    user.favorite_planets.append(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    people = Character.query.get(people_id)
    user = User.query.get(1)
    user.favorite_characters.append(people)
    db.session.commit()
    return jsonify(people.serialize()), 200


@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    planets = list(map(lambda planet : planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    planet = Planet.query.get(planet_id)
    user = User.query.get(1)
    planet_position = user.favorite_planets.index(planet)
    user.favorite_planets.pop(planet_position)
    return jsonify(planet.serialize()),200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_character(people_id):
    people = Character.query.get(people_id)
    user = User.query.get(1)
    character_position = user.favorite_characters.index(people)
    user.favorite_characters.pop(character_position)
    return jsonify(people.serialize()),200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
