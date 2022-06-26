from djongo import models

STATUS_CHOICES = [
    ('NA',"NOT AVAILABLE"),
    ('AV',"AVAILABLE")
]

class BaseModel(models.Model):
    entity_name = models.TextField(max_length=200,blank=True,default="default_base_entity")
    entity_status = models.CharField(choices=STATUS_CHOICES,default='AV',max_length=2)
    
    class Meta:
        abstract = True