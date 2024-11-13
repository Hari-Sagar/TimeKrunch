from django.contrib import admin
from django.urls import path
from .  import views
from .views import *
urlpatterns = [


    path('projects/task/<uuid:pk>/', views.calendarTask, name="SingleTask"),
    #path('', views.home, name="home"),
    path('', views.allTasks, name="alltasks"),
    path('edit_form/', views.EditTask, name='edit_form'),
    path('update_task/<str:pk>/', views.UpdateTask, name='update_form'),
    path('delete_project/<str:pk>/', views.DeleteTask, name='delete_project'), 
    path('create_form/', views.CreateTask, name='create_form')
]