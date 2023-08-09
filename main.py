from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from setup import createAdminIfMissing, randomlyPlacePokemonsOnMap, initializePokemons

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.get("/pokemons/", response_model=list[schemas.Pokemon])
def getPokemons(db: Session = Depends(get_db)):
	pokemons = crud.getPokemons(db=db)
	return pokemons


@app.get("/pokemonsOnMap/", response_model=list[schemas.Pokemon])
def getPokemons(db: Session = Depends(get_db)):
	pokemons = crud.getPokemonsOnMap(db=db)
	return pokemons


@app.get("/users/{user_id}", response_model=schemas.User)
def getUser(user_id: int, db: Session = Depends(get_db)):
	db_user = crud.get_user(db, user_id=user_id)
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return db_user


@app.post("/users/", response_model=schemas.User)
def registerUser(user: schemas.UserCreate, db: Session = Depends(get_db)):
	db_user = crud.getUserByUsername(db, username=user.username)
	if db_user:
		raise HTTPException(status_code=400, detail="Username already registered")
	return crud.create_user(db=db, user=user)


@app.on_event("startup")
def prepareData():
	db = SessionLocal()
	createAdminIfMissing(db=db)
	initializePokemons(db=db)
	randomlyPlacePokemonsOnMap(db=db)
	db.close()

# @app.post("/catchPokemonByUser/{user_id}/", response_model=schemas.MapPokemon)
# def catchPokemon(
# 		user_id: int, pokemon: schemas.PokemonCreate, db: Session = Depends(get_db)
# ):
# 	return crud.catchPokemonByUser(db=db, pokemon=pokemon, user_id=user_id)


# @app.get("/hello/{name}")
# async def say_hello(name: str):
# 	return {"message": f"Hello {name}"}
