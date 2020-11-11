from django.urls import path
from . import views

app_name = 'music'


# music detail along with a key known as the album id
# favorite music detail along with a key known as the album id
# changed the urls to path according the latest django version


urlpatterns = [

    path('',views.home,name='home'),
    path('profile/',views.profileView,name='profile'),
    path('profile-update/',views.profileUpdate,name='profile-update'),
    path('profile-create/',views.profileCreate,name='profile-create'),
    #Signup/Signin
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('index/', views.index, name='index'),

    # Album CRUD
    path('album-list/', views.albumlist, name="album-list"),
    path('album-create/', views.albumCreate, name="album-create"),
    path('album-update/<int:id>', views.albumUpdate, name='album-update'),
    path('album-delete/<int:id>', views.albumDelete, name='album-delete'),
    
    # Song CRUD
    path('song-list/', views.songlist, name="song-list"),
    path('song-create/', views.songCreate, name="song-create"),
    path('song-update/<int:id>', views.songUpdate, name='song-update'),
    path('song-delete/<int:id>', views.songDelete, name='song-delete'),
    
    # music/<album_id>/
    path('detail/<str:album_id>/', views.detail , name='detail'),

    # music/<album_id>/favorite
    path('fav-song/<str:album_id>/', views.favSong , name='fav-song'),
    path('fav-album/', views.favAlbum , name='fav-album'),

    # Favourite list
    path('fav-song-list/', views.favSong_list , name='fav-song-list'),
    path('fav-album-list/', views.favAlbum_list , name='fav-album-list'),
] 
