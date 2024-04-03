from django.contrib import admin
from .models import User, Task, TestCase, Solution

admin.site.register(User)
admin.site.register(Task)
admin.site.register(TestCase)
admin.site.register(Solution)

