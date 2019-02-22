from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('add/', views.add, name='add'),
    path('<int:game_id>/solution/', views.solution, name='solution'),
]
