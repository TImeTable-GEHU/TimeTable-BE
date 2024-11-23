from django.urls import path
from . import views

urlpatterns = [
    path("mongo-status/", views.mongo_status, name="mongo_status"),
    path("postgres-status/", views.postgres_status, name="postgres_status"),
]