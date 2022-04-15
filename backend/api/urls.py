from django.urls import path

from . import views

urlpatterns = [
    path('survivor/add', views.api_add_survivor),
    path('survivor/get-all', views.api_get_all_survivor)
]
