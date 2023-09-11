from django.urls import path
from .views import list_view,like_unlike_post, PostDeleteView, PostUpdateView, post_create

app_name = 'posts'

urlpatterns = [
    path('', list_view, name='main-post-view'),
    path('all/', post_create, name='add-post-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
]
