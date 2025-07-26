from django.urls import path
from app_taiwan_pk import views

app_name = "app_taiwan_pk"

urlpatterns = [
    path("", views.home, name="home"),
    path("api_get_taiwan_pk/", views.api_get_taiwan_pk),
]
