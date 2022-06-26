from django.urls import include, path
from rest_framework import routers 
from .views import BooksModelViewset 

router = routers.DefaultRouter()
router.register(r'books',BooksModelViewset) 


urlpatterns = [ 
    path('',include(router.urls))
]

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# serve static and media files from development server
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)