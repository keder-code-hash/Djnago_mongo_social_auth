from djongo import models
from .Audits import AuditModel
from .BaseModel import BaseModel


class AddressModel(BaseModel):
    name = models.CharField(max_length=255,blank=True,default="default")
    description = models.CharField(max_length = 255, blank = True, default=" default description")
    address_line_1 = models.CharField(max_length=300, blank = True)
    address_line_2 = models.CharField(max_length=300, blank = True)
    street_name = models.CharField(max_length=100,blank=True)
    city_name = models.CharField(max_length=50,blank=True)
    state_name = models.CharField(max_length=50,blank=True)
    country_name = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    ph_NO_code = models.CharField(max_length=50)
    ph_NO = models.CharField(max_length=50)

    audits_data = models.EmbeddedField(model_container=AuditModel) 

    class Meta:
        abstract = True