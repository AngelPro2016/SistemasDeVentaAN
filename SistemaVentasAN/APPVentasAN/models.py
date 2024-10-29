from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def hay_stock(self):
        return self.cantidad_stock > 0

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordenes')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')

    def __str__(self):
        return f'Orden {self.id} - {self.cliente.nombre}'

    def calcular_total(self):
        self.total = sum(item.subtotal() for item in self.detalles.all())
        self.save()

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

class Carrito(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='carrito')
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

    def total_carrito(self):
        return sum(item.subtotal() for item in self.items.all())

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def subtotal(self):
        return self.producto.precio * self.cantidad


