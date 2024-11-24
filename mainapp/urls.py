from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    mongo_status,
    postgres_status,
    getRooms,
    addRoom,
    updateRoom,
    deleteRoom,
)

schema_view = get_schema_view(
    openapi.Info(
        title="GEHU Timetable API",
        default_version="v1",
        description="API for managing timetables and related data",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="vc.vibha23@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("mongo-status/", mongo_status, name="mongo-status"),
    path("postgres-status/", postgres_status, name="postgres-status"),
    path("getRooms/", getRooms, name="get-rooms"),
    path("addRoom/", addRoom, name="add-room"),
    path("updateRoom/<int:pk>/", updateRoom, name="update-room"),
    path("deleteRoom/<int:pk>/", deleteRoom, name="delete-room"),
    path(
        "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
]
