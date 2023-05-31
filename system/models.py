from django.db import models

from utils.models import BaseModel
from account.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# the swipe in the home page
class Swipe(BaseModel):
    # image name
    name = models.CharField(max_length=30)
    img = models.ImageField(max_length=250, upload_to='swipe/%Y%m')
    # image order in the swipe
    order = models.PositiveIntegerField(default=0)

    target_url = models.CharField(max_length=250)

    class Meta:
        # custom table name in the database
        db_table = 'system_swipe'


# ImageRelated can be attraction images or comment images; contenttype is used in this case
class ImageRelated(BaseModel):
    img = models.ImageField(max_length=250, upload_to='images/%Y%m')
    name = models.CharField(max_length=30, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')











