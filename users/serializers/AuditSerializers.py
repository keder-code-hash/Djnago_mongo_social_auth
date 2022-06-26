from rest_framework  import serializers

class AuditModelSerailizers(serializers.Serializer):
    created_at = serializers.DateTimeField()#editable = Flase
    updated_at = serializers.DateTimeField()
    deleted_at = serializers.DateTimeField()
