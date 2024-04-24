from django.db import models


class Upload(models.Model):
    name = models.CharField(max_length=256)
    content_type = models.CharField(max_length=32)
    key = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
