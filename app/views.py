from django.shortcuts import render

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
        return render(request, 'admin/register.html')

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
    return render(request, 'admin/indexAdmin.html')

def RenderTrabajadores(request):
    return render(request, 'admin/trabajadores.html')

def RenderReport(request):
    # FALTA CONCRETAR LOS REPORTES (QUE SE MANDA Y COMO DEPENDIENDO DE CADA TIPO)
    return render(request, 'admin/reportes.html')

def RenderConfig(request):
    return render(request, 'admin/configTienda.html')

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
