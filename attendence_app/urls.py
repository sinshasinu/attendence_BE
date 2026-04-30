from django.urls import path
from .views import AttendanceAPIView, CheckInAPIView, CheckOutAPIView, BreakAPIView


urlpatterns = [
    path('attendance/', AttendanceAPIView.as_view()),
    path('check-in/', CheckInAPIView.as_view()),
    path('check-out/', CheckOutAPIView.as_view()),
    path('break/', BreakAPIView.as_view()),
]