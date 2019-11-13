from django.urls import path
from . import views

urlpatterns = [
    path('sendajax/', views.sendajax,name='sendajax'),
    path('lightson/', views.lightson,name='lightson'),
    path('light1on/', views.light1on,name='light1on'),
    path('light2on/', views.light2on,name='light2on'),
    path('light1off/', views.light1off,name='light1off'),
    path('light2off/', views.light2off,name='light2off'),
    path('lightsoff/', views.lightsoff,name='lightsoff'),
    path('', views.index,name='index'),
]
