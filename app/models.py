from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# UpperCamelCase para las Clases
# snake_case para Metodos
# snake_case para los Atributos de Clases

# Tabla General de Usuarios
class Roles(models.Model):
    nombre = models.CharField(max_length=50)

class Usuario(models.Model):
    nombre = models.CharField(max_length=150, default="")
    apellido = models.CharField(max_length=150, default="")
    # El Username es la parte principal del correo lo que esta antes del @
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    estado = models.CharField(max_length=30)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def set_password(self, raw_password):
        """Establecer la contraseña de forma segura."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verificar la contraseña."""
        return check_password(raw_password, self.password)

# Tablas Admin
class Administrador(Usuario):
    correo = models.EmailField(max_length=255)
    telefono = models.CharField(max_length=16)

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, default="")
    correo = models.EmailField(max_length=255) 
    telefono = models.CharField(max_length=16)
    disponible = models.BooleanField(default=True)

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.DO_NOTHING)
    descripcion = models.TextField()
    fecha_ingreso = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.DO_NOTHING)
    precio_unitario = models.FloatField() 
    disponible = models.BooleanField(default=True)

# Tablas Supervisor
class Supervisor(Usuario):
    area = models.CharField(max_length=50)
    turno = models.CharField(max_length=50)
    equipo = models.ManyToManyField(Usuario, related_name='supervisores')
    disponible = models.BooleanField(default=True)

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    nombre = models.CharField(max_length=150)
    stock_actual = models.IntegerField()
    descripcion = models.TextField()
    fecha_actualizacion = models.DateField()

# Tablas Vendedor
class Vendedor(Usuario):
    nro_ventas = models.IntegerField(default=0)
    supervisor_vendedor = models.ForeignKey(Supervisor, on_delete=models.DO_NOTHING)
    disponible = models.BooleanField(default=True)

class Venta(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.DO_NOTHING)
    nro_boleta = models.IntegerField(default=0)
    rut_cliente = models.CharField(max_length=13)
    fecha = models.DateField()
    total = models.FloatField()
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
    subtotal = models.FloatField()
    