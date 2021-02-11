import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
#from django.urls import reverse


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=50)
    pub_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    visible_priv = models.BooleanField(default=True)
    public = models.BooleanField(default=False)
    share_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description
