from django.db import models

class Post(models.Model):
    #other fields
    class Meta:
        permissions = [
            ('can_publish', 'can publish'),
        ]
