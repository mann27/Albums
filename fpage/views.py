from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from .forms import CreateUserForm,AlbumForm,SongForm
from .models import Album, Song
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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
def home(request):
    return render(request, 'fpage/home.html', context={})


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
def index(request):
    '''Index View for the fpage app. Home page of the app.
        To Show all the albums at avaiable in the DB.'''
    user=request.user
    all_albums = Album.objects.filter(user=user)
    all_songs= Song.objects.filter(user=user)
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
