from django.db import models

# profiles/models.py
class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    next_hour = models.DateTimeField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
