from django.db import models
from core.models.users import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name
    
class Article(models.Model):

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=180, unique=True)

    # SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    # Content
    description = models.TextField()

    # Media
    banner_image = models.ImageField(upload_to='articles/banner/', blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to='articles/thumbnail/', blank=True, null=True)

    # Status
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ArticleFAQ(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='faqs')

    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"FAQ - {self.article.title}"
    
class ArticleHowTo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='howtos')

    step_title = models.CharField(max_length=255)
    step_description = models.TextField()

    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.article.title} - Step {self.order}"
    
    
