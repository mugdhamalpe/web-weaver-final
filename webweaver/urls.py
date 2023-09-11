from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from . views import home_view
from posts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home-view'),
    # path('accounts/', include('allauth.urls')),
    # path('profiles/', include('profiles.urls', namespace='profiles')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('login/', login_view, name='login-view'),
    path('logout/', logout_view, name='logout'),
    path('webteam/', web_team, name="web_team"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)