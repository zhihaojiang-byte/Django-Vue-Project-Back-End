from django.db import models


# almost all models should have these 3 field
class BaseModel(models.Model):
    # in this project, records in the database will not be deleted directly.
    # Instead, change the filed "is_valid" to false.
    is_valid = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


