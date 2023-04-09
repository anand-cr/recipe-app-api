from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import client


class AdminSiteTests(TestCase):
    """Tests for Django admin"""
    # runs before every other test

    # create two users : a superuser and a normal user
    def setUp(self):
        """Create user and client"""
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@exapmle.com',
            password='testpass123',
            name='Test User'
        )

    # we determine the url which list the users,
    def test_users_list(self):
        """Test the users are listed on the page"""

        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        """test to create new user field works"""

        url = reverse('admin:core_user_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
