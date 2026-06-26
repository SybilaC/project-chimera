from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('registro/', views.registro, name='registro'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:servicio_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/quitar/<int:item_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('confirmar-solicitud/', views.confirmar_solicitud, name='confirmar_solicitud'),
    path('admin-productos/', views.admin_productos, name='admin_productos'),
path('admin-productos/crear/', views.crear_servicio, name='crear_servicio'),
path('admin-productos/editar/<int:servicio_id>/', views.editar_servicio, name='editar_servicio'),
path('admin-productos/eliminar/<int:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),
    
]