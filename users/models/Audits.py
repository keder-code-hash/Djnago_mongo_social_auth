from djongo import models
from .BaseModel import BaseModel

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_created=True,auto_now=True)#editable = Flase
    updated_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    deleted_at = models.DateTimeField(auto_created=True,auto_now_add=True)

    class Meta :
        abstract = True