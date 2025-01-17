# Create your models here.
from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) 
    #added profile picture

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True) # Allow drafts
    slug = models.SlugField(unique=True, blank=True) #added slug field
    cover_image = models.ImageField(upload_to='post_covers/', blank=True, null=True) 
    #added cover image

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']  # Order posts by most recent first

class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='subscribers')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'author')  # Prevent duplicate subscriptions

    def __str__(self):
        return f"{self.user.username} subscribes to {self.author.user.username}"
