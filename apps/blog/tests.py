from django.test import TestCase
from django.urls import reverse

from django.conf import settings

from rest_framework.test import APIClient


from .models import Post, Heading, Category, PostAnalytics


### MODELS TESTS ###
class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Tech",
            title="Technology",
            description="All about technology",
            slug="tech"
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Tech')
        self.assertEqual(str(self.category.title), 'Technology')
        self.assertEqual(str(self.category.slug), 'tech')

class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Tech",
            title="Technology",
            description="All about technology",
            slug="tech"
        )
        self.post = Post.objects.create(
            title="Post 1",
            description="All about technology",
            content="Content for the post",
            thumbnail=None,
            keywords="test, post",
            slug="post-1",
            category=self.category,
            status="published"
        )

    def test_post_creation(self):
        self.assertEqual(str(self.post.title), "Post 1")
        self.assertEqual(str(self.category.name), "Tech")
    
    def test_post_published_manager(self):
        self.assertTrue(Post.post_objects.filter(status="published").exists())


class PostAnalyticsModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Analytics", slug="analytics")
        self.post = Post.objects.create(
            title="Analytics Post",
            description="Post for analytics",
            content="Analytics content",
            slug="analytics-post",
            category=self.category
        )
        self.analytics = PostAnalytics.objects.create(post=self.post)

    def test_click_through_rate_update(self):
        self.analytics.increment_impression()
        self.analytics.increment_click()
        self.analytics.refresh_from_db()
        self.assertEqual(self.analytics.click_through_rate, 100.0)


class HeadingModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Heading", slug="heading")
        self.post = Post.objects.create(
            title="Post with Headings",
            description="Post containing headings",
            content="Content with headings",
            slug="post-with-headings",
            category=self.category
        )
        self.heading = Heading.objects.create(
            post=self.post,
            title="Heading 1",
            slug="heading-1",
            level=1,
            order=1
        )

    def test_heading_creation(self):
        self.assertEqual(self.heading.slug, "heading-1")
        self.assertEqual(self.heading.level, 1)


### VIEWS TESTS ###
class PostListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="API", slug="api")
        self.api_key = settings.VALID_API_KEYS[0]
        self.post = Post.objects.create(
            title="API Post",
            description="API post description",
            content="API Content",
            thumbnail=None,
            slug="api-post",
            category=self.category,
            status="published"
        )

    def test_get_post_list(self):
        """
        El lugar al que vamos a hacer la peticion es el name de los urls  name='post-list'),
        """
        url = reverse('post-list')
        response = self.client.get(
            url,
            HTTP_API_KEY=self.api_key
            )

        print(response.json())
        
        data = response.json()
        #self.assertIn
