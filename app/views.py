import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Supervisor, Vendedor,Administrador , Roles, Producto, CategoriaProducto, Proveedor, Inventario
# CamelCase Para las vistas
# snake_case para lo interno

# Control de Acceso
def RenderLogin(request):
    if request.method == "POST":
        pass

    elif request.method == "GET":
        return render(request, 'shared/login.html')

def RenderRegister(request):
    roles = Roles.objects.all()
    vendedores = Vendedor.objects.all()
    supervisores = Supervisor.objects.all()
    if request.method == "POST":
        # USUARIO
        has_error = {}
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('username')
        rol = request.POST.get('rol')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # DE ROLES
        telefono = request.POST.get('telefono')

        supervisor_select = request.POST.get('supervisor')
        turno = request.POST.get('turno')
        equipo = request.POST.getlist('equipo')
        
        # VALIDACIONES GENERALES
        chars_restringidos_correo = [
            ' ', '..', '(', ')', '<', '>', '[',
            ']', ',', ';', ':', '"', '@'
            ]
        
        if nombre.strip() == "":
            has_error['name_empty'] = 'El Campo NOMBRE no Puede Estar Vacio'
        elif len(nombre) > 150:
            has_error['name_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 150'
        else:
            nombre = nombre.title()

        if apellido.strip() == "":
            has_error['ape_empty'] = 'El Campo Apellido no Puede Estar Vacio'
        elif len(apellido) > 150:
            has_error['ape_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 150'
        else:
            apellido = apellido.title()

        if username.strip() == "":
            has_error['username_empty'] = 'El Campo CORREO no Puede Estar Vacio'
        else:
            invalid_char = []
            for char in username:
                if char in chars_restringidos_correo:
                    invalid_char.append(char)
            if len(invalid_char) > 0:
                invalid_char_str = ', '.join(set(invalid_char))
                has_error['username_char_error'] = 'Caracter no Valido: {}.'.format(invalid_char_str)
        
        if rol == '-1':
            has_error['rol_default'] = 'El Campo ROL Debe ser DISTINTO al PREDETERMINADO'

        if password.strip() == "":
            has_error['password_empty'] = 'El Campo Contraseña no Puede Estar Vacio'
        elif len(password) > 128:
            has_error['password_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 128'
        
        if confirm_password.strip() == "":
            has_error['con_pass_empty'] = 'El Campo de Confirmacion de Contraseña no Puede Estar Vacio'
        elif len(confirm_password) > 128:
            has_error['con_pass_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 128'

        if password != confirm_password:
            has_error['password_final'] = 'Las contraseñas no coinciden'

        # VALIDACIONES DE ROL
        
        if rol == '1':
            if telefono.strip() == "":
                has_error['telefono_empty'] = 'El Campo Teléfono no Puede Estar Vacio'
            
        elif rol == '2':
            if supervisor_select == '-1' or supervisor_select == '':
                supervisor = None
                disponible = False
            elif supervisor_select == None:
                has_error['none_error'] = 'Debe Elegir una Opcion, la PREDETERMINADA Cuenta'
            else:
                try:
                    supervisor = Supervisor.objects.get(id=supervisor_select)
                    disponible = True
                except:
                    has_error['not_found'] = 'Supervisor no encontrado'

        elif rol == '3':
            if turno.strip() == "":
                has_error['turno_empty'] = 'El Campo Turno no Puede Estar Vacio'
            elif '-1' in equipo and len(equipo) > 1:
                has_error['equipo_multi'] = 'No se puede seleccionar "Sin equipo" junto con otra opción.'
                    
            if not equipo:
                has_error['equipo_empty'] = 'Debe Seleccionar al Menos un Vendedor o la Opcion Predeterminada'

        # VALIDAR EXISTENCIA DEL OBJETO

        if not has_error:
            if rol == '1':
                user = Administrador(
                    nombre=nombre,
                    apellido=apellido,
                    username=username,
                    rol=Roles.objects.get(id=rol),
                    correo= username + '@nufra.com',
                    telefono=telefono
                )
                user.set_password(password)
                user.save()
            if rol == '2':
                user = Vendedor(
                    nombre=nombre,
                    apellido=apellido,
                    username=username,
                    rol=Roles.objects.get(id=rol),
                    nro_ventas=0,
                    supervisor_vendedor=supervisor,
                    disponible=disponible
                )
                user.set_password(password)
                user.save()

            if rol == '3':
                user = Supervisor(
                    nombre=nombre,
                    apellido=apellido,
                    username=username,
                    rol=Roles.objects.get(id=rol),
                    turno=turno
                )
                user.set_password(password)
                user.save()

                if equipo:
                    equipo_venta = Vendedor.objects.filter(id__in=equipo)
                    user.equipo.set(equipo_venta)

            return render(request, 'admin/views/register.html', {'roles': roles, 'vendedores': vendedores, 'supervisores': supervisores})
        else:
            return render(request, 'admin/views/register.html', {'roles': roles, 'vendedores': vendedores, 'supervisores': supervisores, 'errores': has_error})
    
    elif request.method == "GET":
        return render(request, 'admin/views/register.html', {'roles': roles, 'vendedores': vendedores, 'supervisores': supervisores})

# Usuario General
def RenderUserHome(request):
    return render(request, 'usuario/indexUser.html')

def RenderUserCatalog(request):
    if request.method == 'GET':
        # Filtros para visualizar solo las categorias con productos 
        categorias_con_productos = CategoriaProducto.objects.filter(producto__isnull=False).distinct()
        productos = Producto.objects.filter(categoria__in=categorias_con_productos)

        return render(request, 'usuario/catalog.html', {'categorias': categorias_con_productos, 'productos': productos})

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
        has_error = {}
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
            correo_final = correo.lower() + '@' + dominio.lower()
            proveedor = Proveedor(nombre=nombre, correo=correo_final, telefono=telefono)
            proveedor.save()
            return redirect('addProveedor')
        else:
            return render(request,'admin/proveedores/addProveedor.html', {'errores':has_error})

    elif request.method == 'GET':
        return render(request, 'admin/proveedores/addProveedor.html')

def EditProveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        has_error = {}
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
            correo_final = correo.lower() + '@' + dominio.lower()
            proveedor.nombre = nombre.title()
            proveedor.correo = correo_final
            proveedor.telefono = telefono
            proveedor.save()
            return redirect('proveedores')
        else:
            return render(request,'admin/proveedores/addProveedor.html', {'errores':has_error})
    
    elif request.method == 'GET':
        correo_base = proveedor.correo

        if '@' in correo_base:
            local, dominio = correo_base.split('@')
        else:
            local, dominio = correo_base, ""

        return render(request, 'admin/proveedores/addProveedor.html', {'proveedor': proveedor, 'correo': local, 'dominio': dominio})

def BlockProveedor(request, id):
    if request.method == 'GET':
        proveedor = get_object_or_404(Proveedor, id=id)
        if proveedor.disponible:
            try:
                proveedor.disponible = False
                proveedor.save()
                return redirect('proveedores')
            except:
                return HttpResponse(f"Error al Deshabilitar al Proveedor: {proveedor.nombre}", status=404)
        else:
            try:
                proveedor.disponible = True
                proveedor.save()
                return redirect('proveedores')
            except:
                return HttpResponse("Error al Habilitar al Proveedor: {}".format(proveedor.nombre), status=404)        


# Categorias
def RenderCategorias(request):
    categorias = CategoriaProducto.objects.all()
    if request.method == 'POST':
        has_error = {}
        nombre = request.POST.get('nombre')

        if nombre == "":
            has_error['name_empty'] = 'El NOMBRE NO puede estar VACIO'
        elif len(nombre) > 50:
            has_error['name_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 50'
        else:
            nombre = nombre.title()

        if not has_error:
            categoria = CategoriaProducto(nombre=nombre)
            categoria.save()
            return redirect('categorias')
        else:
            return render(request, 'admin/productos/categorias/categorias.html', {'categorias': categorias, 'errores':has_error})
        
    elif request.method == 'GET':
        return render(request, 'admin/productos/categorias/categorias.html', {'categorias': categorias})

def EditCategoria(request, id):
    categorias = CategoriaProducto.objects.all()
    categoria = get_object_or_404(CategoriaProducto, id=id)

    if request.method == 'POST':
        has_error = {}
        nombre = request.POST.get('nombre')

        # Validaciones de datos
        if not nombre:
            has_error['name_empty'] = 'El NOMBRE NO puede estar VACIO'
        elif len(nombre) > 50:
            has_error['name_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 50'
        else:
            nombre = nombre.title()

        if not has_error:
            categoria.nombre = nombre
            categoria.save()
            return redirect('categorias')
        else:
            return render(request, 'admin/productos/categorias/categorias.html', {
                'categorias': categorias,
                'editable': categoria,
                'errores': has_error
            })

    elif request.method == 'GET':
        return render(request, 'admin/productos/categorias/categorias.html', {
            'categorias': categorias,
            'editable': categoria
        })
    
def BlockCategoria(request, id):
    if request.method == 'GET':
        categoria = CategoriaProducto.objects.get(id=id)
        if categoria.disponible:
            try:
                categoria.disponible = False
                categoria.save()
                return redirect('categorias')
            except:
                return HttpResponse(f"Error al Deshabilitar la Categoria: {categoria.nombre}", status=404)
        else:
            try:
                categoria.disponible = True
                categoria.save()
                return redirect('categorias')
            except:
                return HttpResponse("Error al Habilitar la Categoria: {}".format(categoria.nombre), status=404)        

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
        imagen = request.FILES.get('imagen')

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
                fecha_ingreso=fecha,
                imagen=imagen
            )

            producto.save()
            return redirect('addProducto')
        else:
            return render(request, 'admin/productos/addProducto.html', {'categorias': categorias, 'proveedores': proveedores, 'errores':has_error})
  
    elif request.method == 'GET':
        return render(request, 'admin/productos/addProducto.html', {'categorias': categorias, 'proveedores': proveedores})

def EditProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
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
        imagen = request.FILES.get('imagen')

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

        # Validar Existencia (solo si el nombre ha cambiado)
        if Producto.objects.filter(nombre=nombre).exclude(id=producto.id).exists():
            has_error['duplicado'] = 'Producto ya existente'

        if not has_error:
            # Actualizar el producto
            producto.nombre = nombre
            producto.categoria = get_object_or_404(CategoriaProducto, id=categoria)
            producto.proveedor = get_object_or_404(Proveedor, id=proveedor)
            producto.descripcion = descripcion
            producto.precio_unitario = precio
            producto.fecha_ingreso = fecha
            if imagen:
                producto.imagen = imagen
        
            producto.save()

            return redirect('productos') 
        else:
            return render(request, 'admin/productos/editProducto.html', {
                'categorias': categorias,
                'proveedores': proveedores,
                'producto': producto,
                'errores': has_error
            })
  
    elif request.method == 'GET':
        return render(request, 'admin/productos/addProducto.html', {
            'categorias': categorias,
            'proveedores': proveedores,
            'producto': producto
        })

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
