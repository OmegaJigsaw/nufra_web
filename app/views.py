import datetime

#SESSION
from django.contrib.auth import logout

#HTTP
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

#MODEL
from .models import DetalleVenta, Usuario, Supervisor, Vendedor,Administrador , Roles, Producto, CategoriaProducto, Proveedor, Inventario, Venta


#DECORADORES DE SESSION
def admin_required(view_func):
    """Función decoradora que asegura que el usuario tenga rol de administrador."""
    def wrapper(request, *args, **kwargs):
        """Wrapper protector que valida el rol de administrador antes de permitir el acceso."""
        # rol_id se basan en los de bd
        if request.session.get('user_id') and request.session.get('rol_id') == '1':
            return view_func(request, *args, **kwargs)
        return redirect('Login')  # Redirige al login si no es admin
    return wrapper

def vendedor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id') and request.session.get('rol_id') == '2':  # '2' para rol de vendedor
            return view_func(request, *args, **kwargs)
        return redirect('Login')
    return wrapper

def supervisor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id') and request.session.get('rol_id') == '3':  # '3' para rol de supervisor
            return view_func(request, *args, **kwargs)
        return redirect('Login')
    return wrapper

# Control de Acceso
def RenderLogout(request):
    logout(request)  # Limpia la sesión del usuario
    return redirect('Login')

def RenderLogin(request):
    """ Funcion de Renderizado y Validado del Login """
    if request.method == "POST":
        has_error = {}
        chars_restringidos_user = [
            ' ', '..', '(', ')', '<', '>', '[',
            ']', ',', ';', ':', '"', '@'
            ]
        
        username = request.POST.get('username')

        if username.strip() == "":
            has_error['username_empty'] = 'El Campo Usuario no Puede Estar Vacio'
        elif len(username) > 255:
            has_error['username_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 255'
        else:
            invalid_char = []
            for char in username:
                if char in chars_restringidos_user:
                    invalid_char.append(char)
            if len(invalid_char) > 0:
                invalid_char_str = ', '.join(set(invalid_char))
                has_error['username_char_error'] = 'Caracter no Valido: {}.'.format(invalid_char_str)
        
        password = request.POST.get('password')
        if password.strip() == "":
            has_error['password_empty'] = 'El Campo Contraseña no Puede Estar Vacio'
        elif len(password) > 128:
            has_error['password_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 128'
            
        if not has_error:
            try:
                user = Usuario.objects.get(username=username)
                if user.check_password(password):
                    # SESSION DATA
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['rol_id'] = str(user.rol.id)  

                    if user.rol.id == 1:
                        return redirect('AdminHome')
                    elif user.rol.id == 2:
                        return redirect('Ventas')
                    elif user.rol.id == 3:
                        return redirect('SupHome')
                else:
                    has_error['cred_error'] = 'Las Credenciales no Coinciden'
            except Usuario.DoesNotExist:
                has_error['user_error'] = 'Usuario no Encontrado'
        return render(request, 'shared/login.html', {'errores': has_error})

    elif request.method == "GET":
        return render(request, 'shared/login.html')

@admin_required
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
@admin_required
def RenderAdminHome(request):
    return render(request, 'admin/views/indexAdmin.html')

@admin_required
def RenderTrabajadores(request):
    return render(request, 'admin/views/trabajadores.html')

@admin_required
def RenderReport(request):
    # FALTA CONCRETAR LOS REPORTES (QUE SE MANDA Y COMO DEPENDIENDO DE CADA TIPO)
    return render(request, 'admin/views/reportes.html')

@admin_required
def RenderConfig(request):
    if request.method == 'GET':
        return render(request, 'admin/views/configTienda.html')

# Proveedores
@admin_required
def RenderProveedores(request):
    proveedores = Proveedor.objects.all()
    if request.method == 'GET':
        return render(request, 'admin/proveedores/proveedores.html', {'proveedores': proveedores})

@admin_required
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

@admin_required
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

@admin_required
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
@admin_required
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

@admin_required
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

@admin_required 
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

@admin_required
def RenderProducto(request):
    productos = Producto.objects.all()
    if request.method == 'GET':
        return render(request, 'admin/productos/productos.html', {'productos': productos})

@admin_required 
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

@admin_required
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
@admin_required
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
@supervisor_required
def RenderSupHome(request):
    return render(request, 'supervisor/indexSuper.html')

@supervisor_required
def RenderPanel(request):
    return render(request, 'supervisor/panel.html')

@admin_required
def RenderSupInventario(request):
    inventario = Inventario.objects.all()
    return render(request, 'admin/inventario/inventario.html', {'inventario': inventario})

@admin_required
def AddInventario(request):
    productos = Producto.objects.all()
    has_error = {}
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        stock = request.POST.get('stock_actual')
        fecha = request.POST.get('fecha_actualizacion')

    # Validaciones
        if producto_id == '-1':
            has_error['producto_empty'] = "Debe seleccionar un producto."
        
        if not stock:
            has_error['stock_empty'] = "El stock no puede estar vacío."
        elif not stock.isdigit() or int(stock) < 0:
            has_error['stock_invalid'] = "El stock debe ser un número positivo."

        if not fecha:
            has_error['fecha_empty'] = "La fecha de actualización es obligatoria."
        else:
            try:
                fecha_valida = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
                if fecha_valida > datetime.date.today():
                    has_error['future_date'] = 'La Fecha de Ingreso NO Puede Estar en el FUTURO'
            except ValueError:
                has_error['invalid_date'] = 'Fecha Ingresada Invalida'
        
        if Inventario.objects.filter(producto_id=producto_id).exists():
            has_error['duplicate'] = "Ya existe un inventario para este producto."

        if not has_error:
            producto = Producto.objects.get(id=producto_id)
            nuevo_inventario = Inventario(
                producto=producto,
                nombre=producto.nombre,
                stock_actual=int(stock),
                fecha_actualizacion=fecha
            )
            nuevo_inventario.save()
            return redirect('SupInvent') 
        else:
            return render(request, 'admin/inventario/addInventario.html', {
                'productos': productos,
                'errores': has_error,
            })
    
    elif request.method == 'GET':
        return render(request, 'admin/inventario/addInventario.html', {'productos': productos,})

@admin_required
def EditInventario(request, id):
    inventario = get_object_or_404(Inventario, id=id)  # Obtener el inventario a editar
    productos = Producto.objects.all()  # Obtener todos los productos disponibles
    has_error = {}

    if request.method == 'POST':
        # Obtener los datos del formulario
        producto_id = request.POST.get('producto')
        stock = request.POST.get('stock_actual')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha_actualizacion')

        # Validaciones
        if producto_id == '-1':
            has_error['producto_empty'] = "Debe seleccionar un producto."
        
        if not stock:
            has_error['stock_empty'] = "El stock no puede estar vacío."
        elif not stock.isdigit() or int(stock) < 0:
            has_error['stock_invalid'] = "El stock debe ser un número positivo."

        if not fecha:
            has_error['fecha_empty'] = "La fecha de actualización es obligatoria."
        else:
            try:
                fecha_valida = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
                if fecha_valida > datetime.date.today():
                    has_error['future_date'] = 'La Fecha de Ingreso NO Puede Estar en el FUTURO'
            except ValueError:
                has_error['invalid_date'] = 'Fecha Ingresada Invalida'

        # Si no hay errores, actualizar el inventario
        if not has_error:
            producto = get_object_or_404(Producto, id=producto_id)
            inventario.producto = producto
            inventario.nombre = producto.nombre
            inventario.stock_actual = int(stock)
            inventario.fecha_actualizacion = fecha
            inventario.save()

            return redirect('SupInvent')

        # Si hay errores, renderizar el formulario con los errores
        return render(request, 'admin/inventario/addInventario.html', {
            'productos': productos,
            'inventario': inventario,
            'errores': has_error
        })

    elif request.method == 'GET':
        # Si es una solicitud GET, renderizar el formulario con los datos del inventario
        return render(request, 'admin/inventario/addInventario.html', {
            'productos': productos,
            'inventario': inventario
        })

@supervisor_required
def RenderSupPersonal(request):
    return render(request, 'supervisor/personal.html')

# Vendedor
@vendedor_required
def RenderVenHome(request):
    inventario = Inventario.objects.all()
    return render(request, 'vendedor/indexVendedor.html', {'inventario': inventario})

@vendedor_required
def AgregarCarrito(request):
    has_error = {}
    inventario_actual = Inventario.objects.all()
    carrito = request.session.get('carrito', [])
    if request.method == 'POST':
        codigo = request.POST.get('codigo')

        if not codigo.isnumeric():
            has_error['incorrect_code'] = 'Codigo Incorrecto'

        try:
            cantidad_str = request.POST.get('cantidad')
            cantidad = int(cantidad_str)
            producto = Producto.objects.get(id=codigo)
            inventario = Inventario.objects.get(producto=producto)
            if inventario.stock_actual < cantidad:
                has_error['stock_insuficiente'] = f"No hay suficiente stock para {producto.nombre}. Solo quedan {inventario.stock_actual} unidades disponibles."

        except ValueError:
            has_error['cantidad_value_error'] = 'La Cantidad Debe ser un Numero'
        except Producto.DoesNotExist:
            has_error['producto_404'] = 'Producto no Encontrado'
        except Inventario.DoesNotExist:
            has_error['inventario_404'] = 'Inventario no Disponible para este Producto'

        if not has_error:
            carrito.append({
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio': producto.precio_unitario,
                'subtotal': producto.precio_unitario * cantidad,
            })
            request.session['carrito'] = carrito
            return redirect('Ventas')
        else:
            return render(request, 'vendedor/ventas.html', {'carrito': carrito, 'errores': has_error, 'inventario': inventario_actual})

@vendedor_required
def DeleteItemCarro(request, id):
    carrito = request.session.get('carrito', [])
    carrito = [item for item in carrito if item['producto_id'] != id]
    request.session['carrito'] = carrito
    return redirect('Ventas') 

@vendedor_required
def RenderVentas(request):
    has_error = {}
    carrito = request.session.get('carrito', [])
    total = sum(item['subtotal'] for item in carrito)
    if request.method == 'POST':
        # VALIDAR RUT (REAL)
        rut_cliente = request.POST.get('rut')
        if not rut_cliente or rut_cliente == "":
            has_error['rut_vacio'] = 'El RUT no puede estar Vacio'

        if not carrito:
            has_error['carrito_empty'] = 'El Carrito no Puede Estar Vacio'
            
        if not has_error:
            vendedor_id = request.session.get('user_id')
            vendedor = Vendedor.objects.get(id=vendedor_id)
            fecha_actual = datetime.datetime.now()
            fecha_final = fecha_actual.strftime('%Y-%m-%d')

            venta = Venta(
            vendedor = vendedor,
            rut_cliente = rut_cliente,
            fecha = fecha_final,
            total = total
            )
            venta.save()
            # Generar detalles por item
            for item in carrito:
                producto = Producto.objects.get(id = item['producto_id'])
                inventario = Inventario.objects.get(producto=producto)
                # Agregar Detalles
                detalle = DetalleVenta(
                    venta = venta,
                    producto = producto,
                    cantidad = item['cantidad'],
                    precio_unitario = item['precio'],
                    subtotal = item['subtotal'],
                )
                detalle.save()
                
                # Disminuir stock
                inventario.stock_actual -= item['cantidad']
                # Verificar si el stock es bajo
                if inventario.stock_actual < 15:
                    inventario.estado = 'Bajo'
        
                # Guardar la actualización en inventario
                inventario.save()

            #MANEJAR EL LIMPIADO DEL CARRO SOLAMENTE CUANDO NO HAYAN ERRORES ANTES DEL SAVE
            request.session['carrito'] = []
            return redirect('Ventas') 
        else:
            ventas = Venta.objects.all()
            inventario_actual = Inventario.objects.all()
            return render(request, 'vendedor/ventas.html', {'errores': has_error, 'ventas': ventas, 'carrito': carrito , 'inventario': inventario_actual})

    elif request.method == 'GET':
        inventario_actual = Inventario.objects.all()
        ventas = Venta.objects.all()
        return render(request, 'vendedor/ventas.html', {'ventas': ventas, 'inventario':inventario_actual, 'carrito': carrito})
    
@vendedor_required
def RenderDetalle(request, id):
    venta = Venta.objects.get(id=id)
    detalles = DetalleVenta.objects.filter(venta=venta) 
    return render(request, 'vendedor/detalle.html', {
        'venta': venta,
        'detalle': detalles
    })