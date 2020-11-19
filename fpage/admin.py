
from django.contrib import admin
from .models import Album
from .models import Song
from .models import UserProfile
from .models import Watchlater

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(UserProfile)
admin.site.register(Watchlater)
# Register your models here.
