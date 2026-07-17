from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Post
from api.serializers import PostSerializer


class PostUnitTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="momin",
            password="123456"
        )

    def test_post_create(self):
        post = Post.objects.create(
            author=self.user,
            title='salom',
            content='alik',

        )
        self.assertEqual(post.title, 'salom')
        self.assertEqual(post.author.username, "momin")

    def test_serializer_valid(self):
        serializer = PostSerializer(data={
            'title': 'salom',
            'content': 'bshdghfghefgehfghfee'
        })
        self.assertTrue(serializer.is_valid())

    def test_permission(self):
        response = self.client.post("/api/posts/", {
            'title': 'salom',
            'content': 'smniencienceicnei'
        })
        self.assertIn(response.status_code, [401, 403])


class IntegrationTest(APITestCase):
    def test_api(self):
        register = self.client.post('/api/register/', {
            "username": "ali",
            "password": "123456",
            "confirm_password": "123456"
        })
        self.assertEqual(register.status_code , status.HTTP_201_CREATED)

        token = self.client.post('/api/token/' , {
            "username": "ali",
            "password": "123456"
        })
        self.assertEqual(token.status_code , status.HTTP_200_OK)

        access = token.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )


        post = self.client.post('/api/posts/', {
            'title' : 'salom' ,
            'content' : 'jnejnjencjecnjcnu'

        })
        self.assertEqual(post.status_code , status.HTTP_201_CREATED)
        post_id = post.data['id']

        posts = self.client.get("api/posts/")

        self.assertEqual(posts.status_code, status.HTTP_200_OK)


        update = self.client.put(f"api/posts/{post_id}/", {
            "title": "Yangilandi",
            "content": "abbababababbaabbababababab"
        })

        self.assertEqual(update.status_code, status.HTTP_200_OK)