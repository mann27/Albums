
from django.contrib import admin
from .models import Album
from .models import Song
from .models import favourite

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(favourite)
# Register your models here.
