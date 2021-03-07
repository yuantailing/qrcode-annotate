from django.urls import path

from . import views

app_name = 'annotate'

urlpatterns = [
    path('index', views.index, name='index'),
    path('task/<int:id>', views.task, name='task'),
    path('getimage/<int:id>', views.getimage, name='getimage'),
    path('tokenlogin', views.tokenlogin, name='tokenlogin'),
]
