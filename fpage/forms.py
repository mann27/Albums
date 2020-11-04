from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Album,Song

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
	
class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('artist', 'album_title', 'genre', 'album_logo_link','is_favorite_album')


class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = ('album', 'file_type', 'song_title', 'is_favorite')
    
    def __init__(self, user=None,*args, **kwargs):
        super(SongForm, self).__init__(*args,**kwargs)
        if user:
            self.fields['album'].queryset = Album.objects.filter(user=user)
