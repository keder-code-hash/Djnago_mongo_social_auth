from rest_framework import serializers
from users.serializers.UsersSerializers import UsersModelSerailizers
from users.models.JwtTokwnModels import OutstandingToken


class OutstandingTokenSerializers(serializers.ModelSerializer):
    user = UsersModelSerailizers()
    class Meta: 
        model = OutstandingToken
        fields = "__all__"
        read_only_fields = ('_id',)