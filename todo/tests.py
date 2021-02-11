from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from .models import Item
from .views import itemHomeListView


class ItemTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123',
        )

        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='testuser2@email.com',
            password='testpass123',
        )

        self.item = Item.objects.create(
            description='todo item description',
            author=self.user
        )

        self.item2 = Item.objects.create(
            description='shared item',
            author=self.user,
            visible_priv=False
        )

    def test_correct_view_used(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, itemHomeListView.__name__)

    def test_correct_template_used(self):
        self.client.login(email='testuser@email.com', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_item_is_displayed_for_logged_in_user(self):
        self.client.login(email='testuser@email.com', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'todo item description')
        self.assertNotContains(response, 'blablabla')
        self.assertTemplateUsed(response, 'home.html')

    def test_item_is_displayed_for_logged_out_user(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/' % (reverse('account_login')))

    def test_user_score(self):
        self.client.login(email='testuser@email.com', password='testpass123')
        self.user.score = 37
        response = self.client.get(reverse('home'))
        self.assertContains(response, '37')

    def test_remove_item(self):
        self.client.login(email='testuser@email.com', password='testpass123')
        self.item.visible_priv = False
        self.item.save()
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Empty list')
        self.assertNotContains(response, 'todo item description')

    def test_shared_item_visible_for_follower(self):
        self.user2.friends.add(self.user)
        self.user2.save()
        self.item2.public = True
        self.item2.save()
        self.client.login(email='testuser2@email.com', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'todo item description')
        self.assertContains(response, 'shared item')
        self.assertContains(response, 'Empty list')


# Create your tests here.
