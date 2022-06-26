from djongo import models
from users.models.Audits import AuditModel
from users.models.BaseModel import BaseModel
from users.models.Users import Users
from django import forms
# title, image, author, dateOfPublication, chapters (array),
# price

class Chapters(models.Model):

    index_no      =  models.IntegerField()
    chapter_name  =  models.CharField(max_length=200,blank=False,null=False)
    chapter_desc  =  models.CharField(max_length=400,blank=False,null=False)
    starting_page =  models.IntegerField()
    ending_page   =  models.IntegerField()
    audit_status  =  models.EmbeddedField(model_container=AuditModel)
    entity_details=  models.EmbeddedField(model_container=BaseModel)

    class Meta :
        abstract = True
 

class Boooks(models.Model):

    _id                  = models.ObjectIdField()
    book_name            = models.CharField(max_length=200,blank=False,null=False)
    book_desc            = models.CharField(max_length=400,blank=False,null=False)
    book_image           = models.ImageField(upload_to = 'media')
    date_of_publications = models.DateTimeField()
    price                = models.IntegerField()

    author               = models.ArrayReferenceField(to=Users,
                                on_delete=models.CASCADE,)
    chapters             = models.ArrayField(model_container=Chapters)
    audit_status         = models.EmbeddedField(model_container=AuditModel)
    entity_details       = models.EmbeddedField(model_container=BaseModel)