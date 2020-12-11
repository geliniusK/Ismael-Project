from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Item

class ItemTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
        username='reviewuser',
        email='reviewuser@email.com',
        password='testpass123',
        )

        self.item = Item.objects.create(
        description='todo item description',
        author=self.user
        )

    

# Create your tests here.
