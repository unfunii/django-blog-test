from rest_framework.test import APITestCase
from .models import Tag
from django.contrib.auth import get_user_model

# Create your tests here.

class TagAPITests(APITestCase):
    def test_get_tag_list(self):
        Tag.objects.create(name='Python')
        response = self.client.get('/api/tags/') # self.client - виртуальный браузер
        
        self.assertEqual(response.status_code, 200) # assertEqual(a, b) означает: Проверь, что a равно b.
        self.assertEqual(response.data[0]['name'], 'Python') # response.data — весь список; [0] — первый объект списка; ['name'] — значение его поля name; ожидаемое значение — 'Python'.
        
    def test_create_tag(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(user=user) # 
        
        response = self.client.post(
            '/api/tags/',
            {'name': 'Django'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Tag.objects.filter(name='Django').exists()) 
        
    def test_unauthenticated_user_cannot_create_tag(self):
        response = self.client.post( 
            '/api/tags/',
            {'name': 'Secret'},
            format='json',
        )
        
        self.assertEqual(response.status_code, 401)
        self.assertFalse(
            Tag.objects.filter(name='Secret'). exists()
        )
        