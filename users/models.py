import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    score = models.PositiveIntegerField(default=0)
    friends = models.ManyToManyField('self', blank=True, symmetrical=False)
    new_f = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='msg')

    # def is_friend(self):


    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': str(self.pk)})

# Create your models here.
