from django.urls import path
from .views import MongoStatusView, PostgresStatusView, RoomListView, RoomDetailView

urlpatterns = [
    path("mongo-status/", MongoStatusView.as_view(), name="mongo-status"),
    path("postgres-status/", PostgresStatusView.as_view(), name="postgres-status"),
    path("getRooms/", RoomListView.as_view(), name="get-rooms"),
    path("addRoom/", RoomListView.as_view(), name="add-room"),
    path("updateRoom/<int:pk>/", RoomDetailView.as_view(), name="update-room"),
    path("deleteRoom/<int:pk>/", RoomDetailView.as_view(), name="delete-room"),
]
