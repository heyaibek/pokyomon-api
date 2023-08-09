from pydantic import BaseModel


class PokemonBase(BaseModel):
	title: str
	description: str
	image: str


class PokemonCreate(PokemonBase):
	title: str
	description: str
	image: str


class Pokemon(PokemonBase):
	id: int

	class Config:
		orm_mode: True


class UserPokemon(PokemonBase):
	owner_id: int

	class Config:
		orm_mode: True


class MapPokemon(PokemonBase):
	pokemon_id: int
	lat: float
	lng: float

	class Config:
		orm_mode: True


class UserBase(BaseModel):
	username: str


class UserCreate(UserBase):
	password: str


class User(UserBase):
	id: int
	pokemons: list[UserPokemon] = []

	class Config:
		orm_mode: True
