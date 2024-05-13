from pydantic import BaseModel, FilePath, Field, EmailStr, validator
from pymongo import MongoClient
from pprint import pprint
import os
from datetime import datetime
from typing import Any, List, Union
import requests

#hacer esquema de la bbdd
class Nota(BaseModel):
	rate: float = Field(ge=0., lt=5.)
	count: int = Field(ge=1)
				
class Producto(BaseModel):
	_id: Any
	title: str
	price: float
	description: str
	category: str
	image: str | None
	rating: Nota

	# Validador para asegurarse de que el campo 'title' comienza con mayúscula
	@validator('title')
	def validate_title(cls, value):
		if not value[0].isupper():
			raise ValueError('El título debe comenzar con mayúscula')
		return value

class ProductoCompra(BaseModel):
    productId: Any
    quantity: int

class Compra(BaseModel):
    _id: Any
    userId: Union[EmailStr, int]
    date: datetime
    products: List[ProductoCompra]