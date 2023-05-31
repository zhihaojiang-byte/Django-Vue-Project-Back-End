from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Avg

from utils.models import BaseModel
from account.models import User
from system.models import ImageRelated
from django.contrib import admin


class Attraction(BaseModel):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=240, null=True, blank=True)
    cover_img = models.ImageField(max_length=250, upload_to='attraction/cover_img/%Y%m')
    banner_img = models.ImageField(max_length=250, upload_to='attraction/banner_img/%Y%m/')
    province = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    is_popular = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    images = GenericRelation(ImageRelated, related_query_name="rel_attraction_images")

    @property
    def comments_count(self):
        return self.comments.filter(is_valid=True).count()

    @property
    def images_count(self):
        return self.images.filter(is_valid=True).count()

    @property
    @admin.display()
    def rating(self):
        rating = self.comments.filter(is_valid=True).aggregate(Avg('rating'))['rating__avg']
        if rating is None:
            rating = 0
        return rating

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-update_at']


class AttractionInfo(BaseModel):
    attraction = models.OneToOneField(Attraction, on_delete=models.CASCADE)
    info = RichTextField()


class Comment(BaseModel):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, related_name="comments", on_delete=models.CASCADE)
    content = models.CharField(blank=True, null=True, max_length=500)
    rating = models.FloatField(default=5)

    images = GenericRelation(ImageRelated, related_query_name="rel_comment_images")

    class Meta:
        ordering = ['-update_at']


class Ticket(BaseModel):
    attraction = models.ForeignKey(Attraction, related_name="tickets", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    desc = models.CharField(max_length=120, null=True, blank=True)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    @property
    def sell_price(self):
        return self.price * (1 - self.discount/100)

    @property
    def on_sale(self):
        return self.discount != 0

    def __str__(self):
        return self.name


class TicketInfo(BaseModel):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    info = RichTextField()

