from django.shortcuts import render
from .models import Producto, CategoriaProducto, Proveedor, Inventario

# CamelCase Para las vistas
# snake_case para lo interno

# Control de Acceso
def RenderLogin(request):
    if request.method == "POST":
        pass
    
    elif request.method == "GET":
        return render(request, 'shared/login.html')

def RenderRegister(request):
    if request.method == "POST":
        pass
    
    elif request.method == "GET":
        return render(request, 'admin/views/register.html')

# Usuario General
def RenderUserHome(request):
    return render(request, 'usuario/indexUser.html')

def RenderUserCatalog(request):
    return render(request, 'usuario/catalog.html')

def RenderAbout(request):
    return render(request, 'usuario/about.html')

def RenderFAQ(request):
    return render(request, 'usuario/faq.html')

# Admin
def RenderAdminHome(request):
    return render(request, 'admin/views/indexAdmin.html')

def RenderTrabajadores(request):
    return render(request, 'admin/views/trabajadores.html')

def RenderReport(request):
    # FALTA CONCRETAR LOS REPORTES (QUE SE MANDA Y COMO DEPENDIENDO DE CADA TIPO)
    return render(request, 'admin/views/reportes.html')

def RenderConfig(request):
    if request.method == 'GET':
        return render(request, 'admin/views/configTienda.html')

# Proveedores
def RenderProveedores(request):
    proveedores = Proveedor.objects.all()
    if request.method == 'GET':
        return render(request, 'admin/proveedores/proveedores.html', {'proveedores': proveedores})

def AddProveedor(request):
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        return render(request, 'admin/proveedores/addProveedor.html', {})

# Productos
def RenderProducto(request):
    inventario = Inventario.objects.all()
    if request.method == 'GET':
        return render(request, 'admin/productos/productos.html', {'inventario': inventario})
    
def AddProducto(request):
    categorias = CategoriaProducto.objects.all()
    proveedores = Proveedor.objects.all()
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        return render(request, 'admin/productos/addProducto.html', {'categorias': categorias, 'proveedores': proveedores})

# Supervisor
def RenderSupHome(request):
    return render(request, 'supervisor/indexSuper.html')

def RenderPanel(request):
    return render(request, 'supervisor/panel.html')

def RenderSupInventario(request):
    return render(request, 'supervisor/inventario.html')

def RenderSupPersonal(request):
    return render(request, 'supervisor/personal.html')

# Vendedor
def RenderVenHome(request):
    return render(request, 'vendedor/indexVendedor.html')

def RenderVentas(request):
    return render(request, 'vendedor/ventas.html')
