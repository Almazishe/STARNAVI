from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, UserPostLike



@admin.register(UserPostLike)
class UserPostLikeAdmin(admin.ModelAdmin):
    list_display = ('get_post', 'get_user', 'like', 'unlike', 'updated_at')

    def get_post(self, obj):
        return obj.post.title
    get_post.short_description = "Post"
    
    
    def get_user(self, obj):
        user = obj.user

        if user is not None:
            return user.username
        return None
    get_user.short_description = "User"
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at','get_image')

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="100" style="border-radius: 50%;"')
        return mark_safe(f'<img alt="Нет фото" width="100"')
