from django.urls import path
from .views import MongoStatusView, PostgresStatusView, RoomViewSet

urlpatterns = [
    path("mongo-status/", MongoStatusView.as_view(), name="mongo-status"),
    path("postgres-status/", PostgresStatusView.as_view(), name="postgres-status"),
    path("getRooms/", RoomViewSet.as_view(), name="get-rooms"),
    path("addRoom/", RoomViewSet.as_view(), name="add-room"),
    path("updateRoom/<int:pk>/", RoomViewSet.as_view(), name="update-room"),
    path("deleteRoom/<int:pk>/", RoomViewSet.as_view(), name="delete-room"),

]
