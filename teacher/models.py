from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    address = models.TextField()
    mobile = models.CharField(max_length=20)
    status = models.BooleanField(default=True)  # False = Not Approved, True = Approved

    def __str__(self):
        return self.user.username