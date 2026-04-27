from django.db import models

class categoria_producto(models.Model):
    NombreCategoria = models.CharField(max_length=100, unique=True, verbose_name='Categoría')
    activo_Categoria = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cat_CategoriaProducto'
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'

    def __str__(self):
        return self.NombreCategoria