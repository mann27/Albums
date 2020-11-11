
from django.contrib import admin
from .models import Album
from .models import Song
from .models import UserProfile

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(UserProfile)
# Register your models here.
