import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
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
    has_error = {}
    if request.method == 'POST':
        chars_restringidos_correo = [
            ' ', '..', '(', ')', '<', '>', '[',
            ']', ',', ';', ':', '"', '@'
            ]
        
        chars_restringidos_telefono = [
            'A','B','C','D','E','F','G','H','I','J','K','L',
            'M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ',
            'o','p','q','r','s','t','v','w','x','y','z','.'
            '@','#','!','$','%','^','&','*','_','=',
            '{','}','[',']','/',':',';',',','<','>','|','--'
        ]

        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        dominio = request.POST.get('dominio')
        telefono = request.POST.get('telefono')
        correo_final = ""

        if nombre.strip() == "":
            has_error['name_empty'] = 'El Campo NOMBRE no Puede Estar Vacio'

        if correo.strip() == "":
            has_error['email_empty'] = 'El Campo CORREO no Puede Estar Vacio'
        else:
            invalid_char = []
            for char in correo:
                if char in chars_restringidos_correo:
                    invalid_char.append(char)
            if len(invalid_char) > 0:
                invalid_char_str = ', '.join(set(invalid_char))
                has_error['email_char_error'] = 'Caracter no Valido: {}.'.format(invalid_char_str)
        
        if dominio.strip() == "":
            has_error['dom_empty'] = 'El Dominio del CORREO no Puede Estar Vacio'
        else:
            invalid_char = []
            for char in dominio:
                if char in chars_restringidos_correo:
                    invalid_char.append(char)
            if invalid_char:
                invalid_char_str = ', '.join(set(invalid_char))
                has_error['dom_char_error'] = 'Caracter(es) no Válido(s) en DOMINIO: {}.'.format(invalid_char_str)

        if telefono.strip() == "":
            has_error['phone_empty'] = 'El Campo TELEFONO no Puede Estar Vacio'
        else:
            invalid_char = []
            for char in telefono:
                if char in chars_restringidos_telefono:
                    invalid_char.append(char)
            if invalid_char:
                invalid_char_str = ', '.join(set(invalid_char))
                has_error['phone_char_error'] = 'Caracter(es) no Válido(s) en TELEFONO: {}.'.format(invalid_char_str)
                        
        if not has_error:
            correo_final = correo + '@' + dominio
            proveedor = Proveedor(nombre=nombre, correo=correo_final, telefono=telefono)
            proveedor.save()
            return redirect('addProveedor')
        else:
            return render(request,'admin/proveedores/addProveedor.html', {'errores':has_error})

    elif request.method == 'GET':
        return render(request, 'admin/proveedores/addProveedor.html')

# Productos
def RenderProducto(request):
    productos = Producto.objects.all()
    if request.method == 'GET':
        return render(request, 'admin/productos/productos.html', {'productos': productos})
    
def AddProducto(request):
    categorias = CategoriaProducto.objects.all()
    proveedores = Proveedor.objects.all()
    if request.method == 'POST':
        has_error = {}

        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categoria')
        proveedor = request.POST.get('proveedor')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        fecha = request.POST.get('fecha')

        # Validacion Nombre
        if nombre.strip() == "":
            has_error['name_empty'] = 'El Campo NOMBRE NO Puede Estar Vacio'
        elif len(nombre) > 150:
            has_error['name_max_char'] = 'Se ha Superado el Limite de Caracteres, MAXIMO Permitido: 150'
        elif nombre.isdigit():
            has_error['char_numerico'] = 'El Campo NOMBRE NO Puede ser Solamente NUMERICO'
        else:
            nombre = nombre.title()

        # Validacion Categoria
        if categoria == '-1':
            has_error['cate_default'] = 'El Campo CATEGORIA Debe ser DISTINTO al PREDETERMINADO'
        
        # Validacion Proveedor
        if proveedor == '-1':
            has_error['pro_default'] = 'El Campo Proveedor Debe ser DISTINTO al PREDETERMINADO'

        # Validacion Descripcion
        if descripcion.strip() == "":
            has_error['des_empty'] = 'El Campo Descripcion NO Puede Estar Vacio'
        else:
            descripcion = descripcion.capitalize()

        # Validacion Precio
        if precio.strip() == "":
            has_error['price_empty'] = 'El Campo Precio NO Puede Estar Vacio'
        else:
            try:
                precio = float(precio)
            except ValueError:
                has_error['price_char_error'] = 'El PRECIO Debe ser un Número Válido.'
        
        # Validacion Fecha
        if not fecha:
            has_error['date_empty'] = 'La FECHA NO Puede Esta VACIA'
        else:
            try:
                fecha_valida = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
                if fecha_valida > datetime.date.today():
                    has_error['future_date'] = 'La Fecha de Ingreso NO Puede Estar en el FUTURO'
            except ValueError:
                has_error['invalid_date'] = 'Fecha Ingresada Invalida'

        # Validar Existencia
        if Producto.objects.filter(nombre=nombre).exists():
                has_error['duplicado'] = 'Producto ya existente'

        if not has_error:
            producto = Producto(
                nombre=nombre,
                categoria=get_object_or_404(CategoriaProducto, id=categoria),
                proveedor=get_object_or_404(Proveedor, id=proveedor),
                descripcion=descripcion,
                precio_unitario=precio,
                fecha_ingreso=fecha
            )
            producto.save()
            return redirect('addProducto')
        else:
            return render(request, 'admin/productos/addProducto.html', {'categorias': categorias, 'proveedores': proveedores, 'errores':has_error})
  
    elif request.method == 'GET':
        productos = Producto.objects.all()
        return render(request, 'admin/productos/addProducto.html', {'categorias': categorias, 'proveedores': proveedores})

def EditProducto(request):
    pass



# Manejo de Producto / Para no eliminar registros
def BlockProducto(request, id):
    if request.method == 'GET':
        producto = Producto.objects.get(id=id)
        if producto.disponible:
            try:
                producto.disponible = False
                producto.save()
                return redirect('productos')
            except:
                return HttpResponse(f"Error al deshabilitar el producto: {producto.nombre}", status=404)
        else:
            try:
                producto.disponible = True
                producto.save()
                return redirect('productos')
            except:
                return HttpResponse("Error al habilitar el producto: {}".format(producto.nombre), status=404)        

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
