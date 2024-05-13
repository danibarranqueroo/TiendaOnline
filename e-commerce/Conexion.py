# fichero para la conexión con la api y creación de la bbdd
from pydantic import BaseModel, FilePath, Field, EmailStr, field_validator
from pymongo import MongoClient
from pprint import pprint
import os
from datetime import datetime
from typing import Any, List, Union
import requests

#funcion para bajar los datos de la api
def getProductos(api):
	response = requests.get(api, stream=True)
	return response.json()

#bajar datos de la api
productos = getProductos('https://fakestoreapi.com/products')
compras = getProductos('https://fakestoreapi.com/carts')

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
	image: FilePath | None
	rating: Nota

	# Validador para asegurarse de que el campo 'title' comienza con mayúscula
	@field_validator('title')
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

#conexion con la bbdd
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   
productos_collection = tienda_db.productos  
compras_collection = tienda_db.compras

#borrar lo que hubiera en la bbdd
productos_collection.delete_many({})
compras_collection.delete_many({})

#crear un diccionario para mapear productoid antiguo a nuevo ID de producto
mapeo_productos = {}

#guardar los datos de los productos en la base de datos y hacer el mapeo
for producto in productos:
	id = producto['id']

	# Modificar la URL de la imagen para tener una ruta relativa
	imagen_url = producto['image']
	imagen_nombre = imagen_url.split('/')[-1]
	imagen_ruta_relativa = "imagenes/"+imagen_nombre
	producto['image'] = FilePath(imagen_ruta_relativa)
    
    # Descargar la imagen y guardarla en la carpeta 'imagenes'
	imagen_ruta_absoluta = "imagenes/"+imagen_nombre
	imagen_bytes = requests.get(imagen_url).content
	with open(imagen_ruta_absoluta, 'wb') as imagen_file:
		imagen_file.write(imagen_bytes)

	producto.pop('id', None)
	producto_obj = Producto(**producto)
	producto_dict = producto_obj.dict()
	producto_dict['image'] = str(producto_obj.image)
	producto_dict.pop('_id', None)
	resultado = productos_collection.insert_one(producto_dict)
    
    #obtener el nuevo ID generado por MongoDB
	nuevo_id_producto = resultado.inserted_id
    
    #mapear el productoid antiguo con el nuevo ID
	mapeo_productos[id] = nuevo_id_producto

#actualizar los datos de las compras con los nuevos IDs de productos
for compra in compras:
	compra.pop('id', None)
	for producto_compra in compra['products']:
        #obtener el nuevo ID de producto a partir del mapeo
		nuevo_id_producto = mapeo_productos.get(producto_compra['productId'])
        
        #actualizar el productoid en la compra con el nuevo ID
		producto_compra['productId'] = nuevo_id_producto

    # Crear una instancia de Compra utilizando el esquema definido
	compra_obj = Compra(**compra)
	compras_collection.insert_one(compra_obj.dict())

#verificar la cantidad de documentos en la colección
print(productos_collection.count_documents({}))
print(compras_collection.count_documents({}))