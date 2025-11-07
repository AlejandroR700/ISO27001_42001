from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.features, name='features'),
    path('seguridad/', views.security, name='security'),
    path('contacto/', views.contact, name='contact'),
]
