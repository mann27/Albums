from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from .forms import CreateUserForm,AlbumForm,SongForm,ProfileForm
from .models import Album, Song, UserProfile,Watchlater
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Case, When


# from django.db.models import Q
# Generic method for making a view.

#class IndexView(generic.ListView):
    #template_name='fpage/index.html'
    #context_object_name='all_Albums'
    #def get_queryset(self):
     #   return Album.objects.all()

#class DetailView(generic.DetailView):
  #  model = Album
   # template_name='fpage/detail.html'
def search(request):
    query = request.GET.get("query")
    song = Song.objects.all()
    qs = song.filter(song_title__icontains=query)

    return render(request, 'fpage/search.html', {'songs': qs,"query":query})


def watchlater(request):
    if request.method == "POST":
        user = request.user

        # we are storing the video_id in a variable of same name
        video_id = request.POST['video_id']

        #filtering based on the user
        watch = Watchlater.objects.filter(user=user)

        # for loop for checking if the video is there in watch later if not we will save it
        for i in watch:
            if video_id == i.video_id:
                message = "Your Video is Already Added"
                break
        else:
            watchlater = Watchlater(user=user, video_id=video_id)
            watchlater.save()
            message = "Your Video is Succesfully Added"
    
        song = Song.objects.filter(id=video_id).first()
        return render(request, 'fpage/home.html', {'song': song, "message": message})
    
    # Sorting based on the time and not on the basis of video_id  
    # so if i add a video yesterday and then on today it will show today's video first and yesterday's video second
    wl = Watchlater.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(id__in=ids).order_by(preserved)

    return render(request, 'fpage/watchlater.html', {'song': song})


def home(request):
    return render(request, 'fpage/home.html', context={})

def delete_user(self):
    self.user.delete()
    return redirect('fpage:home')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('fpage:index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('fpage:login')
			

        context = {'form':form}
        return render(request, 'fpage/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('fpage:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('fpage:index')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'fpage/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('fpage:home')

@login_required(login_url='fpage:login')
def profileView(request):
    all_info=UserProfile.objects.filter(user=request.user)
    context={
        'all_info':all_info,
    }
    return render(request,'fpage/profile.html',context)

@login_required(login_url='fpage:login') 
def profileUpdate(request): 
    profile= get_object_or_404(UserProfile, user=request.user)
    form = ProfileForm(initial={'firstname': profile.first_name , 'lastname': profile.last_name, 'email': profile.email, 'phone_num': profile.phone_num, 'fav_genre':profile.fav_genre , 'profile_image':profile.profile_image})
    if request.method == "POST":  
        form = ProfileForm(request.POST, instance=profile)  
        if form.is_valid():  
            try: 
                form.save() 
                model = form.instance
                return redirect('fpage:profile')
            except: 
                messages.error(request, "Error. Profile was not updated")
    messages.success(request, "Profile Updated!" )
    return render(request,'fpage/profile_update.html',{'form':form})

@login_required(login_url='fpage:login')
def profileCreate(request):
    if request.method == "POST":  
            form = ProfileForm(request.POST)
            if form.is_valid():  
                try:  
                    fs=form.save(commit=False)
                    fs.user=request.user
                    fs.save()
                    return redirect('fpage:profile')  
                except:  
                    messages.error(request, "Error. Profile was not created")  
    else:  
        form = ProfileForm()
    messages.success(request, "Profile Created!" )
    return render(request,'fpage/forms.html',{'form':form})

@login_required(login_url='fpage:login')
def index(request):
    '''Index View for the fpage app. Home page of the app.
        To Show all the albums at avaiable in the DB.'''
    user=request.user
    all_albums = Album.objects.filter(user=user)
    template = loader.get_template('fpage/index.html')
    context = {
        'all_albums': all_albums,
    }
    return render(request, 'fpage/index.html', context)

@login_required(login_url='fpage:login')   
def detail(request,album_id):
    
    album = get_object_or_404(Album, id=album_id)
    return render(request, 'fpage/detail.html', {'album' : album})


@login_required(login_url='fpage:login')
def favSong(request, album_id):

     album = get_object_or_404(Album, id=album_id)
     try:
         selected_song = album.song_set.get(id=request.POST['song'])
     except (KeyError, Song.DoesNotExist):
        return render(request, 'fpage/detail.html' ,{
            'album' : album,
            'error_message' : "you did not select a valid song"})
        
     else:
        if selected_song.is_favorite:
            selected_song.is_favorite = False
        else:
            selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'fpage/detail.html', {'album' : album})

@login_required(login_url='fpage:login')
def albumlist(request):
    user=request.user
    all_albums = Album.objects.filter(user=user)
    context = {
        'all_albums': all_albums,
    }
    return render(request, 'fpage/albumadd.html',context)


@login_required(login_url='fpage:login')
def albumCreate(request):  
    if request.method == "POST":  
        form = AlbumForm(request.POST)
        if form.is_valid():  
            try:  
                fs=form.save(commit=False)
                fs.user=request.user
                fs.save()
                return redirect('fpage:index')  
            except:  
                pass  
    else:  
        form = AlbumForm()  
    return render(request,'fpage/forms.html',{'form':form})   

@login_required(login_url='fpage:login') 
def albumUpdate(request, id): 
    album = Album.objects.get(id=id)
    form = AlbumForm(initial={'Title': album.album_title, 'Artist': album.artist, 'Genre': album.genre, 'Logo': album.album_logo_link})
    if request.method == "POST":  
        form = AlbumForm(request.POST, instance=album)  
        if form.is_valid():  
            try: 
                form.save() 
                model = form.instance
                return redirect('fpage:index')
            except Exception as e: 
                pass    
    return render(request,'fpage/forms.html',{'form':form})    

def albumDelete(request, id):
    album = Album.objects.get(id=id)
    try:
        album.delete()
    except:
        pass
    return redirect('fpage:index')

@login_required(login_url='fpage:login')
def songlist(request):
    user=request.user
    all_songs= Song.objects.filter(user=user)
    context = {
        'all_songs': all_songs,
    }
    return render(request, 'fpage/songs.html',context)

@login_required(login_url='fpage:login')
def songCreate(request): 
    if request.method == "POST":
        form = SongForm(request.user,request.POST) 
        if form.is_valid():  
            try:  
                fs=form.save(commit=False) 
                fs.user=request.user
                fs.save()
                return redirect('fpage:index')  
            except:  
                pass  
    else:  
        form = SongForm(user=request.user)  
    return render(request,'fpage/song-forms.html',{'form':form})   

@login_required(login_url='fpage:login') 
def songUpdate(request, id):  
    song = Song.objects.get(id=id)
    form = SongForm(request.user,initial={'album': song.album, 'file type': song.file_type, 'song title': song.song_title, 'favorite': song.is_favorite})
    if request.method == "POST":  
        form = SongForm(request.POST, instance=song)  
        if form.is_valid():  
            try: 
                form.save() 
                model = form.instance
                return redirect('fpage:song-list')
            except Exception as e: 
                pass    
    return render(request,'fpage/song-forms.html',{'form':form})    

def songDelete(request, id):
    song = Song.objects.get(id=id)
    try:
        song.delete()
    except:
        pass
    return redirect('fpage:index')

@login_required(login_url='fpage:login')
def favAlbum(request):
    if request.method == 'GET' and request.is_ajax():

         # use get method to access values in GET request 
        album_id = request.GET.get('album_id', None)   
        album = Album.objects.get(id=album_id)
        if album:
            _fav = album.is_favorite_album

           # if album is already favorite
            if _fav:
                album.is_favorite_album = False
            else:
                album.is_favorite_album = True

            # save album
            album.save()
            # success
            return JsonResponse({}, status=200) 
        else:
            # album not found
            return JsonResponse({}, status=404)   
    # invalid request
    return JsonResponse({}, status=400)


@login_required(login_url='fpage:login')
def favSong_list(request):
    user=request.user
    fav=Song.objects.filter(is_favorite=True,user=user)
    return render(request, 'fpage/favourite_songs.html' , {'fav' : fav}) 

@login_required(login_url='fpage:login')
def favAlbum_list(request):
    user=request.user
    fav=Album.objects.filter(is_favorite_album=True,user=user)
    return render(request, 'fpage/favourite_album.html' , {'fav' : fav})  
    
    """def favAlbum(request, album_id):
    album=get_object_or_404(Album, id=album_id)
    try: 
        selected_album = album.album_set.get(title=request.POST['album']) 
    except (KeyError, Album.DoesNotExist): 
        return render(request, 'fpage/index.html',{
            'album' : album , 
            'error_message' : "you didn't select a valid album"}) 
    else: 
        selected_album.is_favorite1 = True 
        selected_album.save()   
        return render(request, 'fpage/index.html' , {'all_albums' : album})
        """
    
    
    
    """ class BlogSearchListView(BlogListView):
            
            paginate_by = 10

            def get_queryset(self):
                result = super(BlogSearchListView, self).get_queryset()

                query = self.request.GET.get('q')
                if query:
                    query_list = query.split()
                    result = result.filter(
                        reduce(operator.and_,
                            (Q(title__icontains=q) for q in query_list)) |
                        reduce(operator.and_,
                            (Q(content__icontains=q) for q in query_list))
                    )

                return result """
