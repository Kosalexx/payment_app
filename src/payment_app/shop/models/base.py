from django.db import models


class BaseModel(models.Model):
    """Describes the fields and attributes of the Base model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Describes class metadata."""

        abstract = True
