from django.urls import path
from . import views

urlpatterns = [
        path('update-timetable/', views.updateTimeTable, name='update-timetable'),
        path('current-timetable/<str:course_id>/<int:semester>/', views.getCurrentTimeTable, name='get-current-timetable'),
        path('historical-timetables/<str:course_id>/<int:semester>/', views.getHistoricalTimeTable, name='get-historical-timetables'),
]
