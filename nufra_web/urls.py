from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
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
    path('home/admin/trabajadores/', vistas.RenderTrabajadores, name='Trabajadores'),
    path('home/admin/reportes/', vistas.RenderReport, name='Reportes'),
    path('home/admin/configuraciones/', vistas.RenderConfig, name='Config'),

    #Proveedor
    path('home/admin/config/proveedores/', vistas.RenderProveedores, name='proveedores'),
    path('home/admin/config/add-proveedor/', vistas.AddProveedor, name='addProveedor'),
    path('home/admin/config/edit-proveedor/<int:id>/', vistas.EditProveedor, name='editProveedor'),
    #Block/Unblock Proveedor
    path('home/admin/config/block-proveedor/<int:id>/', vistas.BlockProveedor, name='blockProveedor'),
    
    #Producto
    path('home/admin/config/productos/', vistas.RenderProducto, name='productos'),
    path('home/admin/config/add-producto/', vistas.AddProducto, name='addProducto'),
    path('home/admin/config/edit-producto/<int:id>/', vistas.EditProducto, name='editProducto'),
    #Block/Unblock Producto
    path('home/admin/config/productos/block-producto/<int:id>/', vistas.BlockProducto, name='blockProducto'),

    #Categorias
    path('home/admin/config/productos/categorias/', vistas.RenderCategorias, name='categorias'),
    path('home/admin/config/productos/categorias/edit-categoria/<int:id>/', vistas.EditCategoria, name='editCategoria'),
    #Block/Unblock categoria
    path('home/admin/config/productos/categorias/block-categoria/<int:id>/', vistas.BlockCategoria, name='blockCategoria'),

    # Supervisor
    path('home/supervisor/', vistas.RenderSupHome, name='SupHome'),
    path('home/supervisor/panel/', vistas.RenderPanel, name='SupPanel'),
    path('home/supervisor/inventario/', vistas.RenderSupInventario, name='SupInvent'),
    path('home/supervisor/personal/', vistas.RenderSupPersonal, name='SupPersonal'),
    # Vendedor
    path('home/vendedor/', vistas.RenderVenHome, name='VenHome'),
    path('home/vendedor/ventas/', vistas.RenderVentas, name='Ventas'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
