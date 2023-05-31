from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import BaseModel


class User(AbstractUser):
    avatar = models.ImageField(max_length=250, upload_to="avatar/%Y%m", default="avatar/default/avatar.png", null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True, error_messages={
            "unique": "A user with that email already exists.",
        })




