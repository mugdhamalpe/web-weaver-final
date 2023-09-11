from django.urls import path
from posts.views import *
from .views import ( 
    my_profile_view, 
    ProfileDetailView,
)

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('login/', login, name='login-view'),
]