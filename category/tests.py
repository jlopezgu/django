from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category


class CategoryTests(APITestCase):
    url = '/category/'

    def test_create_category(self):
        """
        Ensure we can create a new category object.
        """
        data = {'name': 'Sports'}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Sports')

    def test_list_categories(self):
        """
        Ensure we can get categories list.
        """
        Category.objects.create(name='Sports')

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Sports')