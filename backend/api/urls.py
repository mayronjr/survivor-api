from django.urls import path

from . import views

urlpatterns = [
    path('survivor/add', views.api_add_survivor),
    path('survivor/get/<int:id>', views.api_get_one_survivor),
    path('survivor/get-all', views.api_get_all_survivor),
    path('survivor/update-location/<int:id>', views.api_update_survivor_location),
    path('survivor/relate-infection', views.api_relate_infection),
    path('trade', views.trade)
]
