from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "activo")
    search_fields = ("nombre",)
    list_filter = ("activo",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sku",
        "nombre",
        "categoria",
        "precio_compra",
        "precio_venta",
        "stock",
        "stock_minimo",
        "activo",
    )

    search_fields = ("nombre", "sku")
    list_filter = ("categoria", "activo")
    readonly_fields = ("stock", "fecha_creacion")