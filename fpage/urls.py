from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

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

    path('account-delete/', views.delete_user, name="account-delete"),

    path('index/', views.index, name='index'),

    #Watch-Later
    path('watchlater/', views.watchlater, name='watchlater'),

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

    #Reset
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',success_url=reverse_lazy('fpage:profile')), 
        name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
] 
