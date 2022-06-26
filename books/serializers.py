from .models import Boooks 

from users.serializers.AuditSerializers import AuditModelSerailizers
from users.serializers.BaseSerializers import BaseModelSerailizers
from users.serializers.UsersSerializers import UsersModelSerailizers

from rest_framework import serializers

class ChapterSerializers(serializers.Serializer):

    index_no      =  serializers.IntegerField()
    chapter_name  =  serializers.CharField()
    chapter_desc  =  serializers.CharField()
    starting_page =  serializers.IntegerField()
    ending_page   =  serializers.IntegerField()
    audit_status  =  AuditModelSerailizers()
    entity_details=  BaseModelSerailizers()

class BookSerializers(serializers.ModelSerializer):
    author         = serializers.ListField(child = UsersModelSerailizers() , required = False , default = [])
    chapters       = serializers.ListField(child = ChapterSerializers() , required = False , default = [])
    audit_status   =  AuditModelSerailizers()
    entity_details =  BaseModelSerailizers()

    class Meta :
        model = Boooks
        fields = "__all__"
        read_only_fields = ('_id',)
