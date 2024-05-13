from django.urls import path
import logging
logger = logging.getLogger(__name__)
from . import views
from polls.api import api

urlpatterns = [
    path("consultas/", views.index, name="index"),
    path("consultas/c1/", views.c1, name="c1"),
    path("consultas/c2/", views.c2, name="c2"),
    path("consultas/c3/", views.c3, name="c3"),
    path("consultas/c4/", views.c4, name="c4"),
    path("consultas/c5/", views.c5, name="c5"),
    path("consultas/c6/", views.c6, name="c6"),
    path("", views.portada, name="portada"),
    path("busqueda/", views.busqueda, name="busqueda"),
    path("buscar-categoria/ropahombre", views.ropahombre, name="ropahombre"),
    path("buscar-categoria/ropamujer", views.ropamujer, name="ropamujer"),
    path("buscar-categoria/joyeria", views.joyeria, name="joyeria"),
    path("buscar-categoria/electronica", views.electronica, name="electronica"),
    path("add/", views.añadir, name="añadir"),
    path("api/", api.urls),
]

# Al añadir la url de django auth se han creado automaticamente todo lo siguiente:
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']