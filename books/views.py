from .models import Boooks
from .serializers import BookSerializers

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from djongo.models.fields import ObjectId
from django.shortcuts import get_object_or_404 
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ModelViewSet

class BooksModelViewset(ModelViewSet): 
    queryset = Boooks.objects.all()
    serializer_class = BookSerializers
    lookup_field  = "_id"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        try: 

            filter_kwargs = {self.lookup_field: ObjectId(self.kwargs[lookup_url_kwarg])}

            fabrixes_data = get_object_or_404(queryset, **filter_kwargs)
            self.check_object_permissions(self.request, fabrixes_data)
        except:
            message = f"Inavalid request: Book Not Found: {self.kwargs[self.lookup_field]}"
            # log.error(message) 
            raise APIException({"message": ValueError(message)}, 400)
        return fabrixes_data
 