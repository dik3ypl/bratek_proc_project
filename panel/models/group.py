from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    join_code = models.CharField(max_length=12, unique=True, verbose_name=_("Join code"))
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_groups',
        verbose_name=_("Group creator")
    )
    image = models.ImageField(upload_to='group_images/', blank=True, null=True, verbose_name=_("Image"))

    def __str__(self):
        return self.name
