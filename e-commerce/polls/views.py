from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
import logging
import pymongo
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .schemas import *
from pathlib import Path
logger = logging.getLogger(__name__)

consultas = [
    ('c1', 'Consulta 1'),
    ('c2', 'Consulta 2'),
    ('c3', 'Consulta 3'),
    ('c4', 'Consulta 4'),
    ('c5', 'Consulta 5'),
    ('c6', 'Consulta 6'),
]

# parte relacionada con la practica 2
def portada(request):
    logger.debug('Debug en pagina inicio')
    logger.info('Carga pagina inicio')
    context = {}
    return render(request, "polls/index.html", context)

def busqueda(request):
    busqueda = request.GET.get('busqueda').lower()
    resultados = Busqueda(busqueda)
    context = {
        'busqueda': busqueda,
        'resultados': resultados,
    }
    return render(request, "polls/search.html", context)

def ropahombre(request):
    ropahombre = RopaHombre()
    context = {
        'ropahombre': ropahombre,
    }
    return render(request, "polls/ropahombre.html", context)

def ropamujer(request):
    ropamujer = RopaMujer()
    context = {
        'ropamujer' : ropamujer,
    }
    return render(request, "polls/ropamujer.html", context)

def joyeria(request):
    joyeria = Joyeria()
    context = {
        'joyeria' : joyeria,
    }
    return render(request, "polls/joyeria.html", context)

def electronica(request):
    electronica = Electronica()
    context = {
        'electronica' : electronica,
    }
    return render(request, "polls/electronica.html", context)

def añadir(request):
    form = ProductoForm()
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug(form.cleaned_data)
            logger.debug(request.FILES)
            # Guarda la imagen en la carpeta static/carpeta-img
            imagen = form.cleaned_data['imagen']
            fs = FileSystemStorage(location='static/carpeta-img')
            filename = fs.save(imagen.name, imagen)
            image_path = Path('static/carpeta-img') / filename  # Crea un objeto Path con la ruta completa al archivo
            image_path_str = str(image_path)   # Convierte el objeto Path a una cadena

            # Verifica que el archivo se guardó correctamente
            if not image_path.is_file():
                raise ValueError(f"El archivo {image_path} no se guardó correctamente")

            # Crea un objeto Producto con los datos del formulario y la imagen
            producto = Producto(
                title=form.cleaned_data['nombre'],
                price=form.cleaned_data['precio'],
                description=form.cleaned_data['descripcion'],
                image=image_path_str,  # Guarda la cadena en lugar del objeto Path
                category=form.cleaned_data['categoria'],  # Añade la categoría aquí
                rating=Nota(rate=4, count=1),  # Añade la calificación aquí
            )

            # Guarda el producto en MongoDB
            producto_dict = {
                'title': producto.title,
                'price': producto.price,
                'description': producto.description,
                'image': str(image_path_str.replace('static/', '')),
                'category': producto.category,
                'rating': {
                    'rate': producto.rating.rate,
                    'count': producto.rating.count,
                },
            }

            client = MongoClient('mongo', 27017)
            tienda_db = client.tienda
            productos_collection = tienda_db.productos
            productos_collection.insert_one(producto_dict)

            # Devuelve la página de éxito
            return redirect('portada')

        else:
            form = ProductoForm()

        return render(request, 'formulario.html', {'form': form})
    context = {
        'form': form,
    }
    return render(request, "polls/añadir.html", context)

# parte relacionada con la practica 1
def index(request):
    # Crea una lista de enlaces a las consultas
    enlaces = []
    for consulta in consultas:
        enlace = f'<li><a href="/consultas/{consulta[0]}">{consulta[1]}</a></li>'
        enlaces.append(enlace)

    # Devuelve la página de inicio con los enlaces a las consultas
    return HttpResponse('<h1>Consultas</h1><ul>' + ''.join(enlaces) + '</ul>', content_type='text/html')

def c1(request):
    salida = Consulta1()
    return HttpResponse(salida)

def c2(request):
    salida = Consulta2()
    return HttpResponse(salida)

def c3(request):
    salida = Consulta3()
    return HttpResponse(salida)

def c4(request):
    salida = Consulta4()
    return HttpResponse(salida)

def c5(request):
    salida = Consulta5()
    return HttpResponse(salida)

def c6(request):
    salida = Consulta6()
    return HttpResponse(salida)