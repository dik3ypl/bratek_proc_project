from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.title


class TestCase(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return f"Test case for {self.task.title}"