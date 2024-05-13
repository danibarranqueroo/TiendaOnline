from django.db import models
from pymongo import MongoClient
from pprint import pprint
from bson.objectid import ObjectId
import logging
logger = logging.getLogger(__name__)

#conexion con la bbdd
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   
productos_collection = tienda_db.productos  
compras_collection = tienda_db.compras

# Funciones de la práctica 3

def obtener_productos(desde, hasta):
    productos = list(productos_collection.find().skip(desde).limit(hasta))
    for producto in productos:
        producto["id"] = str(producto.get('_id'))
        del producto["_id"]
    return productos

def añadir_producto(payload):
    producto_id = productos_collection.insert_one(payload.dict()).inserted_id
    producto = productos_collection.find_one({"_id": producto_id})
    producto["id"] = str(producto.get('_id'))
    del producto["_id"]
    return producto

def obtener_producto_por_id(id):
    producto = productos_collection.find_one({"_id": ObjectId(id)})
    producto["id"] = str(producto.get('_id'))
    del producto["_id"]
    return producto

def modificar_producto(id, payload):
    productos_collection.update_one({"_id": ObjectId(id)}, {"$set": payload.dict()})
    producto = productos_collection.find_one({"_id": ObjectId(id)})
    producto["id"] = str(producto.get('_id'))
    del producto["_id"]
    return producto

def eliminar_producto(id):
    delete_result = productos_collection.delete_one({"_id": ObjectId(id)})
    return delete_result.deleted_count == 1

def modificar_rating(id, new_rating):
    producto = productos_collection.find_one({"_id": ObjectId(id)})
    old_rating = producto.get('rating').get('rate')
    rating_count = producto.get('rating').get('count')

    # Calcular la nueva media
    updated_rating = ((old_rating * rating_count) + new_rating) / (rating_count + 1)

    # Actualizar la calificación y el recuento de calificaciones
    productos_collection.update_one({"_id": ObjectId(id)}, {"$set": {"rating.rate": updated_rating, "rating.count": rating_count + 1}})

    # Recuperar el producto actualizado
    producto = productos_collection.find_one({"_id": ObjectId(id)})
    producto["id"] = str(producto.get('_id'))
    del producto["_id"]
    return producto

# Consultas de la práctica 2

def RopaHombre():
    consulta_ropahombre = {
        'category': 'men\'s clothing'
    }
    resultados_ropahombre = productos_collection.find(consulta_ropahombre).sort('rating.rate', -1)
    
    # Crear una nueva lista para almacenar los resultados modificados
    resultados_modificados = []
    
    for producto in resultados_ropahombre:
        # Cambiar el nombre del campo _id a id
        producto['id'] = producto.pop('_id')
        
        # Añadir el producto modificado a la nueva lista
        resultados_modificados.append(producto)
    
    return resultados_modificados

def RopaMujer():
    consulta_ropamujer = {
        'category': 'women\'s clothing'
    }
    resultados_ropamujer = productos_collection.find(consulta_ropamujer).sort('rating.rate', -1)
    return [{'id': x.pop('_id'), **x} for x in resultados_ropamujer]

def Joyeria():
    consulta_joyeria = {
        'category': 'jewelery'
    }
    resultados_joyeria = productos_collection.find(consulta_joyeria).sort('rating.rate', -1)
    return [{'id': x.pop('_id'), **x} for x in resultados_joyeria]

def Electronica():
    consulta_electronica = {
        'category': 'electronics'
    }
    resultados_electronica = productos_collection.find(consulta_electronica).sort('rating.rate', -1)
    return [{'id': x.pop('_id'), **x} for x in resultados_electronica]

def Busqueda(busqueda):
    consulta_busqueda = {
        'description': {'$regex': busqueda, '$options': 'i'}
    }
    resultados_busqueda = productos_collection.find(consulta_busqueda)
    return [{'id': x.pop('_id'), **x} for x in resultados_busqueda]



# Consultas de la práctica 1
def Consulta1():
    consulta_electronica = {
        'category': 'electronics',
        'price': {'$gte': 100, '$lte': 200}
    }

    resultados_electronica = productos_collection.find(consulta_electronica).sort('price', 1)

    salida = "Consulta 1 -> "
    for producto_electronica in resultados_electronica:
        salida = salida + (f"Nombre: {producto_electronica['title']}, Categoría: {producto_electronica['category']}, Precio: {producto_electronica['price']}€, ")
    return salida

def Consulta2():
    consulta_pocket = {
    'description': {'$regex': 'pocket', '$options': 'i'}
    }

    resultados_pocket = productos_collection.find(consulta_pocket)

    salida = "Consulta 2 -> "
    for producto_pocket in resultados_pocket:
        salida = salida + (f"Nombre: {producto_pocket['title']}, Descripción: {producto_pocket['description']}, ")
    return salida

def Consulta3():
    consulta_puntuacion = {
    'rating.rate': {'$gt': 4}
    }

    resultados_puntuacion = productos_collection.find(consulta_puntuacion)

    salida = "Consulta 3 -> "
    for producto_puntuacion in resultados_puntuacion:
        salida = salida + (f"Nombre: {producto_puntuacion['title']}, Puntuación: {producto_puntuacion['rating']['rate']}, ")
    return salida

def Consulta4():
    consulta_ropa_hombre = {
    'category': 'men\'s clothing'
    }

    resultados_ropa_hombre = productos_collection.find(consulta_ropa_hombre).sort('rating.rate', -1)

    salida = "Consulta 4 -> "
    for producto_ropa_hombre in resultados_ropa_hombre:
        salida = salida + (f"Nombre: {producto_ropa_hombre['title']}, Categoría: {producto_ropa_hombre['category']}, Puntuación: {producto_ropa_hombre['rating']['rate']}, ")
    return salida

def Consulta5():   
    total_facturacion = 0
    for compra in compras_collection.find():
        for producto in compra['products']:
            total_facturacion += producto['quantity'] * productos_collection.find_one({'_id': producto['productId']})['price']

    # Mostrar los resultados
    salida = (f'\nConsulta 5 -> Facturación total: {total_facturacion}€')
    return salida

def Consulta6():
    facturacion_categoria = {}
    for compra in compras_collection.find():
        for producto in compra['products']:
            categoria = productos_collection.find_one({'_id': producto['productId']})['category']
            if categoria not in facturacion_categoria:
                facturacion_categoria[categoria] = 0
            facturacion_categoria[categoria] += producto['quantity'] * productos_collection.find_one({'_id': producto['productId']})['price']

    salida = "Consulta 6 -> "
    for categoria, facturacion in facturacion_categoria.items():
        salida = salida + (f"Categoría: {categoria}, Facturación: {facturacion}€, ")
    return salida