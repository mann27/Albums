from django.urls import include,path
from django.contrib import admin

# base url patters which directs to admin page and the main page of the app
# changed the urls to path according the latest django version 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fpage.urls', namespace='fpage')),
]
