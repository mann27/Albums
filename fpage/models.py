from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre =models.CharField(max_length=100)
    album_logo_link=models.CharField(max_length=1000)
    is_favorite_album = models.BooleanField(default=False)
    #is_favorite1 = models.BooleanField(default=False)
    def __str__ (self):
        return self.album_title+'-'+self.artist

class Song(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title= models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__ (self):
        return self.song_title 

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.CharField(max_length=150)
    phone_num=PhoneNumberField(null=False, blank=False, unique=True)
    fav_genre=models.CharField(max_length=50)
    profile_image = models.ImageField(default='profile.jpeg',null=True, blank=True)