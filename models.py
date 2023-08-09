from sqlalchemy import Column, Integer, String, ForeignKey, Double
from sqlalchemy.orm import relationship

from database import Base


class Pokemon(Base):
	__tablename__ = "pokemons"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	description = Column(String, index=True)
	image = Column(String, index=True)


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True)
	hashed_password = Column(String)


class UserPokemon(Pokemon):
	__tablename__ = "user_pokemons"

	id = Column(Integer, primary_key=True, index=True)
	pokemon_id = Column(Integer, ForeignKey("pokemons.id"))
	user_id = Column(Integer, ForeignKey("users.id"))

	pokemon = relationship("Pokemon", foreign_keys=[pokemon_id])
	user = relationship("User", foreign_keys=[user_id])


class MapPokemons(Base):
	__tablename__ = "map_pokemons"

	id = Column(Integer, primary_key=True, index=True)
	pokemon_id = Column(Integer, ForeignKey("pokemons.id"))
	lat = Column(Double)
	lng = Column(Double)

	pokemon = relationship("Pokemon", foreign_keys=[pokemon_id])
