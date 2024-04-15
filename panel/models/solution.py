from django.db import models
from django.contrib.auth.models import User
from .task import Task


class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    solution_file = models.FileField(upload_to='solutions/')
    test_results = models.JSONField(null=True, blank=True)
    tests_passed = models.BooleanField(default=False)
