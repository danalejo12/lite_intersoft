
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import F

from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm


# =========================================
# PRODUCTOS
# =========================================

# READ: Listar productos
@login_required
@permission_required("core.view_producto", raise_exception=True)
def producto_lista(request):
    productos = Producto.objects.select_related(
        "categoria"
    ).order_by("nombre")

    return render(request, "products/producto_lista.html", {
        "productos": productos
    })


# CREATE: Crear producto
@login_required
@permission_required("core.add_producto", raise_exception=True)
def producto_crear(request):

    if request.method == "POST":
        formulario = ProductoForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "Producto registrado correctamente."
            )

            return redirect("producto_lista")

    else:
        formulario = ProductoForm()

    return render(request, "products/producto_form.html", {
        "formulario": formulario,
        "titulo": "Registrar producto"
    })


# UPDATE: Editar producto
@login_required
@permission_required("core.change_producto", raise_exception=True)
def producto_editar(request, pk):

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        formulario = ProductoForm(
            request.POST,
            instance=producto
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "Producto actualizado correctamente."
            )

            return redirect("producto_lista")

    else:
        formulario = ProductoForm(instance=producto)

    return render(request, "products/producto_form.html", {
        "formulario": formulario,
        "titulo": "Editar producto"
    })


# DELETE: Eliminar producto
@login_required
@permission_required("core.delete_producto", raise_exception=True)
def producto_eliminar(request, pk):

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        # No borramos físicamente el producto.
        # Lo desactivamos para conservar su historial.
        producto.activo = False
        producto.save(update_fields=["activo"])

        messages.success(
            request,
            "Producto desactivado correctamente."
        )

        return redirect("producto_lista")

    return render(
        request,
        "products/producto_confirmar_eliminar.html",
        {"producto": producto}
    )


# =========================================
# CATEGORÍAS
# =========================================

# READ: Listar categorías
@login_required
@permission_required("core.view_categoria", raise_exception=True)
def categoria_lista(request):

    categorias = Categoria.objects.all().order_by("nombre")

    return render(request, "products/categoria_lista.html", {
        "categorias": categorias
    })


# CREATE: Crear categoría
@login_required
@permission_required("core.add_categoria", raise_exception=True)
def categoria_crear(request):

    if request.method == "POST":
        formulario = CategoriaForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "Categoría registrada correctamente."
            )

            return redirect("categoria_lista")

    else:
        formulario = CategoriaForm()

    return render(request, "products/categoria_form.html", {
        "formulario": formulario,
        "titulo": "Registrar categoría"
    })


# UPDATE: Editar categoría
@login_required
@permission_required("core.change_categoria", raise_exception=True)
def categoria_editar(request, pk):

    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "POST":
        formulario = CategoriaForm(
            request.POST,
            instance=categoria
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "Categoría actualizada correctamente."
            )

            return redirect("categoria_lista")

    else:
        formulario = CategoriaForm(instance=categoria)

    return render(request, "products/categoria_form.html", {
        "formulario": formulario,
        "titulo": "Editar categoría"
    })


@login_required
def inicio(request):
    productos_activos = Producto.objects.filter(activo=True)

    return render(request, "index.html", {
        "total_productos": productos_activos.count(),
        "total_categorias": Categoria.objects.filter(activo=True).count(),
        "stock_bajo": productos_activos.filter(
            stock__lte=F("stock_minimo")
        ).count(),
        "ultimos_productos": Producto.objects.select_related(
            "categoria"
        ).order_by("-fecha_creacion")[:5],
    })