import uuid

from django.db import models

# from django.conf import settings
from django.contrib.auth import get_user_model
from django.conf import settings

CustomUserModel = get_user_model()  # settings.AUTH_USER_MODEL


class Link(models.Model):
    # id = models.IntegerField()
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(CustomUserModel, null=True, on_delete=models.CASCADE)
