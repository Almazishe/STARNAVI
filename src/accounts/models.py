from django.db import models
from django.contrib.auth import get_user_model

from utils.models import BaseModel, DateModel


User = get_user_model()


class ActionLog(BaseModel, DateModel):

    user = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)
    action_text = models.TextField()

    
    def __str__(self) -> str:
        return f"{self.user.username}:\n{self.action_text}" 


    class Meta:
        verbose_name = 'User action'
        verbose_name_plural = 'Users actions'
        ordering = ('-created_at',)
    

    @staticmethod
    def act(user: User, text: str):
        action_log = ActionLog(
            user=user,
            action_text=text
        )

        return action_log.save()