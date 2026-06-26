from django.contrib import admin
from .models import Categoria, Servicio, Carrito, ItemCarrito, Orden, ItemOrden

admin.site.register(Categoria)
admin.site.register(Servicio)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Orden)
admin.site.register(ItemOrden)