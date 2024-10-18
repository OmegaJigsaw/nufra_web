from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# UpperCamelCase para las Clases
# snake_case para Metodos
# snake_case para los Atributos de Clases

# Tabla General de Usuarios
# AbstractUser es una clase prehecha que tiene cosas montadas, sirve para manejar herencia
# El username(150 char), password(128 char), first_name(150 char), last_name(150 char) vienen incluidas 
# Al igual que algunos metodos (setter & getter) y atributos solo se llama a la hora de crear el objeto

class Roles(models.Model):
    nombre = models.CharField(max_length=50)

class Usuario(models.Model):
    nombre = models.CharField(max_length=150, default="")
    apellido = models.CharField(max_length=150, default="")
    username = models.CharField(max_length=50, unique=True)
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

class ProductoProveedor(models.Model):
    nombre = models.CharField(max_length=50)

class Proveedor(models.Model):
    correo = models.EmailField(max_length=255) 
    telefono = models.CharField(max_length=16)
    productos = models.ManyToManyField(ProductoProveedor)

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    stock = models.IntegerField(default=0)
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
    