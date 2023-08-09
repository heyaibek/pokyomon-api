from sqlalchemy.orm import Session

import models
import schemas


def getUser(db: Session, user_id: int):
	return db.query(models.User).filter(models.User.id == user_id).first()


def getUserByUsername(db: Session, username: str):
	return db.query(models.User).filter(models.User.username == username).first()


def createUser(db: Session, user: schemas.UserCreate):
	fake_hashed_password = user.password + "notreallyhashed"
	db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def createPokemon(db: Session, pokemonCreate: schemas.PokemonCreate):
	pokemon = models.Pokemon(
		title=pokemonCreate.title,
		description=pokemonCreate.description,
		image=pokemonCreate.image
	)

	db.add(pokemon)
	db.commit()
	db.refresh(pokemon)

	return pokemon

def createMapPokemon(db: Session, pokemon: schemas.MapPokemon):
	db_pokemon = models.MapPokemons(
		pokemon_id = pokemon.pokemon_id,
		lat = pokemon.lat,
		lng = pokemon.lng
	)

	db.add(db_pokemon)
	db.commit()
	db.refresh(db_pokemon)

	return db_pokemon


def clearPokemons(db: Session):
	db.query(models.Pokemon).delete()


def clearPokemonsOnMap(db: Session):
	db.query(models.MapPokemons).delete()


def getPokemons(db: Session):
	return db.query(models.Pokemon).all()


def getPokemonsOnMap(db: Session):
	return db.query(models.MapPokemons).all()


def catchPokemonByUser(db: Session, pokemon: schemas.MapPokemon, user_id: int):
	# get pokemon data by id
	# do roll dicing
	# if won, check if user has pokemon already
	# if user has, do nothing
	# if user doesn't have, add to list
	# if loose, continue
	# re-position pokemon

	db_pokemon = models.UserPokemon(**pokemon.dict(), owner_id=user_id)
	db.add(db_pokemon)
	db.commit()
	db.refresh(db_pokemon)
	return db_pokemon
