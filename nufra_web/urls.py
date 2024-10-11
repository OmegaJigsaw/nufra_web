from django.contrib import admin
from django.urls import path
from app import views as vistas

urlpatterns = [
    # Principal
    path('', vistas.RenderUserHome, name='home'),
    # Control de acceso
    path('login/', vistas.RenderLogin, name='LogIn'),
    path('register/', vistas.RenderRegister, name='Register'),
    # Usuario
    path('catalogo/', vistas.RenderUserCatalog, name='Catalog'),
    path('acerca-de/', vistas.RenderAbout, name='About'),
    path('preguntas-frecuentes/', vistas.RenderFAQ, name='FAQ'),
    # Admin
    path('home/admin/', vistas.RenderAdminHome, name='AdminHome'),
    path('home/admin/trabajadores', vistas.RenderTrabajadores, name='Trabajadores'),
    path('home/admin/reportes', vistas.RenderReport, name='Reportes'),
    path('home/admin/configuraciones', vistas.RenderConfig, name='Config'),
    # Supervisor
    path('home/supervisor/', vistas.RenderSupHome, name='SupHome'),
    path('home/supervisor/panel', vistas.RenderPanel, name='SupPanel'),
    path('home/supervisor/inventario', vistas.RenderSupInventario, name='SupInvent'),
    path('home/supervisor/personal', vistas.RenderSupPersonal, name='SupPersonal'),
    # Vendedor
    path('home/vendedor/', vistas.RenderVenHome, name='VenHome'),
    path('home/vendedor/ventas', vistas.RenderVentas, name='Ventas'),
]
