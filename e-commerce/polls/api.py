from ninja import NinjaAPI, Schema, Query
from typing import List
from pymongo import MongoClient
from bson.objectid import ObjectId
from .models import obtener_productos, añadir_producto, obtener_producto_por_id, modificar_producto, eliminar_producto, modificar_rating

api = NinjaAPI()

class Rate(Schema):
    rate: float
    count: int

class ProductSchema(Schema):  # sirve para validar y para documentación
    id:    str
    title: str
    price: float
    description: str
    category: str
    image: str = None
    rating: Rate

class ProductSchemaIn(Schema):
    title: str
    price: float
    description: str
    category: str
    rating: Rate

class ErrorSchema(Schema):
    message: str

class PaginationQuery(Schema):
    desde: int = 0
    hasta: int = 4

@api.get("/productos", tags=['TIENDA DAI'], response={200: List[ProductSchema]})
def lista_productos(request, desde: int = 0, hasta: int = 4):
    try:
        productos = obtener_productos(desde, hasta)
        return 200, productos
    except:
        return 404, {'message': 'producto no encontrado'}

@api.post("/productos", tags=['TIENDA DAI'], response={201: ProductSchema, 400: ErrorSchema})
def añade_producto(request, payload: ProductSchemaIn):
    try:
        producto = añadir_producto(payload)
        return 201, producto
    except:
        return 400, {'message': 'error al añadir producto'}

@api.get("/productos/{id}", tags=['TIENDA DAI'], response={200: ProductSchema, 404: ErrorSchema})
def detalle_producto(request, id: str):
    try:
        producto = obtener_producto_por_id(id)
        return 200, producto
    except:
        return 404, {'message': 'producto no encontrado'}

@api.put("/productos/{id}", tags=['TIENDA DAI'], response={202: ProductSchema, 404: ErrorSchema})
def modifica_producto(request, id: str, payload: ProductSchemaIn):
    try:
        producto = modificar_producto(id, payload)
        return 202, producto
    except:
        return 404, {'message': 'producto no encontrado'}

@api.delete("/productos/{id}", tags=['TIENDA DAI'], response={204: None, 404: ErrorSchema})
def borra_producto(request, id: str):
    try:
        resultado = eliminar_producto(id)
        if resultado:
            return 204, None
        else:
            return 404, {'message': 'producto no encontrado'}
    except:
        return 404, {'message': 'producto no encontrado'}
    
@api.put('/productos/{id}/{rating}', tags=['TIENDA DAI'], response={202 : ProductSchema, 404 : ErrorSchema})
def modifica_rating(request, id : str, rating : int):
	try:
		producto = modificar_rating(id, rating)
		return 202, producto
	except:
		return 404, {'message': 'producto no encontrado'}