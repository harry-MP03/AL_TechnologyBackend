from django.db import models
from Apps.Catalogos.CategoriaProducto.models import categoria_producto

class ServicioProducto(models.Model):
    NombreProducto = models.CharField(max_length=150, verbose_name='Nombre del Producto/Servicio')
    categoria = models.ForeignKey(
        categoria_producto, 
        on_delete=models.PROTECT,
        verbose_name= 'Categoría'
    )
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Base')
    descripcionProducto = models.TextField(blank=True, null=True)
    activo_producto = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cat_Servicios_Productos'
        verbose_name = 'Servicio o Producto'
        verbose_name_plural = 'Servicios o Productos'
    
    def __str__(self):
        return f"{self.NombreProducto} - ${self.precio_base}"
    