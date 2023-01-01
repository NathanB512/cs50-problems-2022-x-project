from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

# Class for storing diary submissions
class DiarySubmission(models.Model):
    # User, foreign key
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diary")
    # Content
    content = models.TextField(null=False, blank=False)
    # Date added, (datetime field, auto_now_add)
    submissionDate = models.DateTimeField(auto_now_add=True)
