from django .http import Http404
from django .http import HttpResponse
from django .template import loader 
from django .shortcuts import render,get_object_or_404
from django.views import generic
from .models import Album, Song
#from django.db.models import Q



# Generic method for making a view.

#class IndexView(generic.ListView):
    #template_name='fpage/index.html'
    #context_object_name='all_Albums'
    #def get_queryset(self):
     #   return Album.objects.all()

#class DetailView(generic.DetailView):
  #  model = Album
   # template_name='fpage/detail.html'

def index(request):
    all_albums= Album.objects.all()

    template = loader.get_template('fpage/index.html')
    context = {
        'all_albums' : all_albums,
    }
    return render(request, 'fpage/index.html', context)
   
def detail(request,album_id):
    
    album = get_object_or_404(Album, id=album_id)
    return render(request, 'fpage/detail.html', {'album' : album})

def favorite(request, album_id):

     album = get_object_or_404(Album, id=album_id)
     try:
         selected_song = album.song_set.get(id=request.POST['song'])
     except (KeyError, Song.DoesNotExist):
        return render(request, 'fpage/detail.html' ,{
            'album' : album,
            'error_message' : "you did not select a valid song"})
        
     else:
        selected_song.is_favorite =True
        selected_song.save()
        return render(request, 'fpage/detail.html', {'album' : album})

     
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
