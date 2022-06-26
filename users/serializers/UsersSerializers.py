from ..models.Users import Users 

from .AddressSerializers import AddressModelSerailizers
from .AuditSerializers import AuditModelSerailizers
from .BaseSerializers import BaseModelSerailizers

from rest_framework import serializers

class UsersModelSerailizers(BaseModelSerailizers, serializers.ModelSerializer):
    address = serializers.ListField(child = AddressModelSerailizers() , required = False , default = [])
    audits_data = AuditModelSerailizers() 

    class Meta :
        model = Users
        fields = "__all__"
        read_only_fields = ('_id',)
