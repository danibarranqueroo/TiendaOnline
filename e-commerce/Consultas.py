#Realización de las consultas
from pymongo import MongoClient
from pprint import pprint

#conexion con la bbdd
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   
productos_collection = tienda_db.productos  
compras_collection = tienda_db.compras

# Consulta1: Electrónica entre 100 y 200€, ordenados por precio
consulta_electronica = {
    'category': 'electronics',
    'price': {'$gte': 100, '$lte': 200}
}

resultados_electronica = productos_collection.find(consulta_electronica).sort('price', 1)

# Mostrar los resultados
print('Consulta 1 -> Electrónica entre 100 y 200€, ordenados por precio:')
for producto_electronica in resultados_electronica:
    print(f"Nombre: {producto_electronica['title']}, Categoría: {producto_electronica['category']}, Precio: {producto_electronica['price']}€")


# Consulta2: Productos que contengan la palabra 'pocket' en la descripción
consulta_pocket = {
    'description': {'$regex': 'pocket', '$options': 'i'}
}

resultados_pocket = productos_collection.find(consulta_pocket)

# Mostrar los resultados
print('\nConsulta 2 -> Productos con la palabra "pocket" en la descripción:')
for producto_pocket in resultados_pocket:
    print(f"Nombre: {producto_pocket['title']}, Descripción: {producto_pocket['description']}")


# Consulta3: Productos con puntuación mayor de 4
consulta_puntuacion = {
    'rating.rate': {'$gt': 4}
}

resultados_puntuacion = productos_collection.find(consulta_puntuacion)

# Mostrar los resultados
print('\nConsulta 3 -> Productos con puntuación mayor de 4:')
for producto_puntuacion in resultados_puntuacion:
    print(f"Nombre: {producto_puntuacion['title']}, Puntuación: {producto_puntuacion['rating']['rate']}")


# Consulta4: Ropa de hombre, ordenada por puntuación
consulta_ropa_hombre = {
    'category': 'men\'s clothing'
}

resultados_ropa_hombre = productos_collection.find(consulta_ropa_hombre).sort('rating.rate', -1)

# Mostrar los resultados
print('\nConsulta 4 -> Ropa de hombre ordenada por puntuación:')
for producto_ropa_hombre in resultados_ropa_hombre:
    print(f"Nombre: {producto_ropa_hombre['title']}, Categoría: {producto_ropa_hombre['category']}, Puntuación: {producto_ropa_hombre['rating']['rate']}")


# Consulta5: Facturación total
total_facturacion = 0
for compra in compras_collection.find():
    for producto in compra['products']:
        total_facturacion += producto['quantity'] * productos_collection.find_one({'_id': producto['productId']})['price']

# Mostrar los resultados
print(f'\nConsulta 5 -> Facturación total: {total_facturacion}€')

# Consulta6: Facturación por categoría de producto
facturacion_categoria = {}
for compra in compras_collection.find():
    for producto in compra['products']:
        categoria = productos_collection.find_one({'_id': producto['productId']})['category']
        if categoria not in facturacion_categoria:
            facturacion_categoria[categoria] = 0
        facturacion_categoria[categoria] += producto['quantity'] * productos_collection.find_one({'_id': producto['productId']})['price']

# Mostrar los resultados
print('\nConsulta 6 -> Facturación por categoría de producto:')
for categoria, facturacion in facturacion_categoria.items():
    print(f"Categoría: {categoria}, Facturación: {facturacion}€")

