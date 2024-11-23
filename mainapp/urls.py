from django.urls import path
from . import views

urlpatterns = [
    path("mongo-status/", views.mongo_status),
    path("postgres-status/", views.postgres_status),
    path("getRooms/", views.getRooms),
    path("addRoom/", views.addRoom),
    path("updateRoom/<int:pk>/", views.updateRoom),
    path("deleteRoom/<int:pk>/", views.deleteRoom),
]
