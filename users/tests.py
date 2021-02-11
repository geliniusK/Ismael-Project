from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from .forms import CustomUserCreationForm
from .views import (
    SignupPageView,
    FollowingListView,
    FollowersListView,
)


class CustomUserTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testname',
            email='test@email.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'testname')
        self.assertEqual(user.email, 'test@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='testsuper',
            email='super@email.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'testsuper')
        self.assertEqual(user.email, 'super@email.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class SignupTest(TestCase):

    username = 'newuser'
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'not the text')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(
            get_user_model().objects.all()[0].username, self.username
        )
        self.assertEqual(
            get_user_model().objects.all()[0].email, self.email
        )


class FollowPagesTest(TestCase):

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
        self.user2.friends.add(self.user)
        self.user2.save()

        self.user3 = get_user_model().objects.create_user(
            username='testuser3',
            email='testuser3@email.com',
            password='testpass123',
        )

        self.client.login(email='testuser@email.com', password='testpass123')

    def test_status_code_following_list(self):
        response = self.client.get(reverse('following_list'))
        self.assertEqual(response.status_code, 200)

    def test_status_code_followers_list(self):
        response = self.client.get(reverse('followers_list'))
        self.assertEqual(response.status_code, 200)

    def test_follower_list_template(self):
        response = self.client.get(reverse('followers_list'))
        self.assertTemplateUsed(response, 'followers_list.html')

    def test_following_list_template(self):
        response = self.client.get(reverse('following_list'))
        self.assertTemplateUsed(response, 'following_list.html')

    def test_follower_list_resolves_view(self):
        view = resolve('/accounts/followers/')
        self.assertEqual(view.func.__name__, FollowersListView.as_view().__name__)

    def test_following_list_resolves_view(self):
        view = resolve('/accounts/following/')
        self.assertEqual(view.func.__name__, FollowingListView.as_view().__name__)

    def test_follower_list_content(self):
        response = self.client.get(reverse('followers_list'))
        self.assertContains(response, 'testuser2')
        self.assertNotContains(response, 'testuser3')

    def test_following_list_content(self):
        self.client.logout()
        self.client.login(email='testuser2@email.com', password='testpass123')
        response = self.client.get(reverse('following_list'))
        self.assertContains(response, 'testuser')
        self.assertNotContains(response, 'testuser3')

    def test_followers_list_redirected_if_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('followers_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/accounts/followers/' % (reverse('account_login')))

    def test_following_list_redirected_if_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('following_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/accounts/following/' % (reverse('account_login')))

    def test_search_page_redirected_if_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('user_search'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/accounts/search/' % (reverse('account_login')))

    def test_search_page_status_code_search_list(self):
        response = self.client.get('%s?q=' % (reverse('user_search')))
        self.assertEqual(response.status_code, 200)

    def test_search_page_finds_user(self):
        response = self.client.get('%s?q=testuser2' % (reverse('user_search')))
        self.assertContains(response, 'testuser2')
        self.assertNotContains(response, 'testuser3')

# Create your tests here.
