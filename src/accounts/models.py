from django.db import models
from django.contrib.auth import get_user_model

from utils.models import BaseModel, DateModel


User = get_user_model()


class ActionLog(BaseModel, DateModel):
    LOGIN = '_LOGIN_'
    REGISTER = '_REGISTER_'
    CREATE_POST = '_CREATE_POST_'
    GET = '_GET_'
    LIKE = '_LIKE_'
    UNLIKE = '_UNLIKE_'
    REMOVE_LIKE = '_REMOVE_LIKE_'
    ACTION_TYPE_CHOICES = (
        (LOGIN, 'Login'),
        (REGISTER, 'Register'),
        (CREATE_POST, 'Create Post'),
        (GET, 'Get request'),
        (LIKE, 'Like'),
        (UNLIKE, 'Unlike'),
        (REMOVE_LIKE, "Remove like of dislike")
    )

    user = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)
    action_text = models.TextField()
    action_type = models.CharField(max_length=100, choices=ACTION_TYPE_CHOICES, null=True)

    
    def __str__(self) -> str:
        return f"{self.user.username}:\n{self.action_text}" 


    class Meta:
        verbose_name = 'User action'
        verbose_name_plural = 'Users actions'
        ordering = ('-created_at',)
    

    @staticmethod
    def act(user: User, action_type: str, text: str):
        action_log = ActionLog(
            user=user,
            action_text=text,
            action_type=action_type
        )

        return action_log.save()