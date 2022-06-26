from ..models.BaseModel import BaseModel
from rest_framework import serializers

class BaseModelSerailizers(serializers.Serializer):
    entity_name = serializers.CharField()
    entity_status = serializers.CharField()
