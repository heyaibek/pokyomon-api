import random

import requests
from geopy import Point
from geopy.distance import geodesic
from sqlalchemy.orm import Session

import crud
import schemas

radius = 2000
center = Point(51.73213, -1.20631)


def createAdminIfMissing(db: Session):
	admin = crud.getUserByUsername(db=db, username="admin")
	if not admin:
		crud.createUser(db=db, user=schemas.UserCreate(
			username="admin",
			password="admin"
		))


# top left: 42.918307, 74.501686
# bottom right: 42.814837, 74.700562
# center: 42.867961, 74.604284

def generatePoint(center: Point, radiusInKM: int) -> Point:
	random_distance = random.random() * radiusInKM
	random_bearing = random.random() * 360
	return geodesic(kilometers=random_distance).destination(center, random_bearing)


def randomlyPlacePokemonsOnMap(db: Session):
	crud.clearPokemonsOnMap(db=db)

	center = Point(42.867961, 74.604284)

	for pokemon in crud.getPokemons(db=db):
		for i in range(1, 11):
			point = generatePoint(center=center, radiusInKM=25)
			crud.createMapPokemon(db=db, pokemon=schemas.MapPokemon(
				pokemon_id=pokemon.id,
				lat=point.latitude,
				lng=point.longitude
			))


def initializePokemons(db: Session):
	crud.clearPokemons(db=db)

	for num in range(1, 11):
		url = f"https://pokeapi.co/api/v2/pokemon/{num}"
		response = requests.get(url)
		response_json = response.json()

		title = str(response_json['name'])
		description = str(response_json['name'])
		image = str(response_json['sprites']['other']['official-artwork']['front_default'])

		dto = schemas.PokemonCreate(title=title, description=description, image=image)
		crud.createPokemon(db=db, pokemonCreate=dto)
