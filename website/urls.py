from django.contrib import admin
from django.urls import include, path

# base url patters which directs to admin page and the main page of the app
# changed the urls to path according the latest django version 
urlpatterns = [
    path('admin/', admin.site.urls),
    # fpage app urls and namespaced by fpage
    path('', include('fpage.urls', namespace='fpage')),
    path('', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
]
