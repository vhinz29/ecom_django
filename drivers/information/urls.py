from django.urls import path
from . import views

urlpatterns = [
    path('info', views.info, name='info'),
    path('info_delete', views.info_delete, name='info_delete'),
    path('info_register', views.info_register, name='info_register'),
    path('info_date/<infos>/<picks>/', views.info_date, name='info_date'),

]