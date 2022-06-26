from rest_framework import serializers
from .AuditSerializers import AuditModelSerailizers
from .BaseSerializers import BaseModelSerailizers

class AddressModelSerailizers(BaseModelSerailizers):
    name = serializers.CharField()
    description = serializers.CharField()
    address_line_1 = serializers.CharField()
    address_line_2 = serializers.CharField()
    street_name = serializers.CharField()
    city_name = serializers.CharField()
    state_name = serializers.CharField()
    country_name = serializers.CharField()
    zip_code = serializers.CharField()
    ph_NO_code = serializers.CharField()
    ph_NO = serializers.CharField()

    audits_data = AuditModelSerailizers()
