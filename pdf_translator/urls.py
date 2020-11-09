from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('read', views.read, name='read'),

    path('', views.index, name='index'),
]
