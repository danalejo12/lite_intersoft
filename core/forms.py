from django import forms

from .models import Categoria, Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion", "activo"]


class ProductoForm(forms.ModelForm):
    # El stock no se edita aquí: se modifica con movimientos de inventario.
    class Meta:
        model = Producto
        fields = [
            "categoria",
            "sku",
            "nombre",
            "descripcion",
            "precio_compra",
            "precio_venta",
            "stock_minimo",
            "activo",
        ]
