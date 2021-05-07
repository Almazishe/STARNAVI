from django.db import models
from django.utils.text import slugify 
from django.contrib.auth import get_user_model

from utils.models import BaseModel, DateModel

User = get_user_model()



class Post(BaseModel, DateModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='posts')
    text = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.title} | {self.owner.username}'
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class UserPostLike(BaseModel, DateModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')

    like = models.BooleanField(default=False)
    unlike = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username} | {self.post.title} | {self.like} | {self.unlike}'
    
    class Meta:
        verbose_name = 'User post like'
        verbose_name_plural = 'Users posts likes'
        ordering = ("-updated_at",)
