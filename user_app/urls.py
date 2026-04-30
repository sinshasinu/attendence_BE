from .views import UserAPIViews, LoginAPI
from django.urls import path

urlpatterns = [
    path('users/', UserAPIViews.as_view(), name='user-list-create'),
    path('login/', LoginAPI.as_view(), name='login'),

]