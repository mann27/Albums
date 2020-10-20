from django.urls import path
from . import views

app_name = 'music'


# music detail along with a key known as the album id
# favorite music detail along with a key known as the album id
# changed the urls to path according the latest django version


urlpatterns = [
    #/music/
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('', views.index, name='index'),
    path('add-album/', views.add_album, name="add-album"),
    # music/<album_id>/
    path('detail/<str:album_id>/', views.detail , name='detail'),

    # music/<album_id>/favorite
    path('favorite/<str:album_id>/', views.favorite , name='favorite'),
] 