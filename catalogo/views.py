from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Servicio, Carrito, ItemCarrito, Orden, ItemOrden
from .forms import RegistroUsuarioForm, ServicioForm


def catalogo(request):
    servicios = Servicio.objects.filter(disponible=True)

    return render(
        request,
        'catalogo/catalogo.html',
        {
            'servicios': servicios
        }
    )


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            messages.success(
                request,
                "Usuario registrado correctamente. Ahora puedes iniciar sesión."
            )

            return redirect('login')

    else:
        form = RegistroUsuarioForm()

    return render(
        request,
        'catalogo/registro.html',
        {
            'form': form
        }
    )


@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    return render(
        request,
        'catalogo/carrito.html',
        {
            'carrito': carrito
        }
    )


@login_required
def agregar_al_carrito(request, servicio_id):
    servicio = get_object_or_404(
        Servicio,
        id=servicio_id,
        disponible=True
    )

    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        servicio=servicio
    )

    if not creado:
        item.cantidad += 1
        item.save()

    messages.success(
        request,
        f"{servicio.nombre} fue agregado a la solicitud."
    )

    return redirect('ver_carrito')


@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(
        ItemCarrito,
        id=item_id,
        carrito__usuario=request.user
    )

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))

        if cantidad > 0:
            item.cantidad = cantidad
            item.save()
            messages.success(
                request,
                "Cantidad actualizada correctamente."
            )
        else:
            messages.error(
                request,
                "La cantidad debe ser mayor a 0."
            )

    return redirect('ver_carrito')


@login_required
def quitar_del_carrito(request, item_id):
    item = get_object_or_404(
        ItemCarrito,
        id=item_id,
        carrito__usuario=request.user
    )

    item.delete()

    messages.success(
        request,
        "Servicio eliminado de la solicitud."
    )

    return redirect('ver_carrito')
@login_required
def confirmar_solicitud(request):
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    if not carrito.items.exists():
        messages.error(
            request,
            "No puedes confirmar una solicitud vacía."
        )
        return redirect('ver_carrito')

    orden = Orden.objects.create(
        usuario=request.user,
        total=carrito.total()
    )

    for item in carrito.items.all():
        ItemOrden.objects.create(
            orden=orden,
            servicio=item.servicio,
            cantidad=item.cantidad,
            precio_unitario=item.servicio.precio
        )

    carrito.items.all().delete()

    messages.success(
        request,
        "Solicitud confirmada correctamente."
    )

    return render(
        request,
        'catalogo/confirmacion.html',
        {
            'orden': orden
        }
    )
def es_admin(user):
    return user.is_staff


@user_passes_test(es_admin)
def admin_productos(request):
    servicios = Servicio.objects.all()

    return render(
        request,
        'catalogo/admin_productos.html',
        {
            'servicios': servicios
        }
    )


@user_passes_test(es_admin)
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Servicio creado correctamente."
            )
            return redirect('admin_productos')
    else:
        form = ServicioForm()

    return render(
        request,
        'catalogo/formulario_servicio.html',
        {
            'form': form,
            'titulo': 'Crear servicio'
        }
    )


@user_passes_test(es_admin)
def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Servicio actualizado correctamente."
            )
            return redirect('admin_productos')
    else:
        form = ServicioForm(instance=servicio)

    return render(
        request,
        'catalogo/formulario_servicio.html',
        {
            'form': form,
            'titulo': 'Editar servicio'
        }
    )


@user_passes_test(es_admin)
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        servicio.delete()
        messages.success(
            request,
            "Servicio eliminado correctamente."
        )
        return redirect('admin_productos')

    return render(
        request,
        'catalogo/eliminar_servicio.html',
        {
            'servicio': servicio
        }
    )