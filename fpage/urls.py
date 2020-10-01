from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    #/music/
    path('index/', views.index, name='index'),

    # music/<album_id>/
    path('detail/<str:album_id>/', views.detail , name='detail'),

    # music/<album_id>/favorite
    path('favorite/<str:album_id>/', views.favorite , name='favorite'),
] 