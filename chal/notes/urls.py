from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
     path('notes/delete/', views.delete_notes, name='delete_notes'),
    path('view/', views.show_notes, name='show_notes'),
    path('create/', views.make_note, name='make_note'),
    path("" , views.say_hello , name='welcome')
]

