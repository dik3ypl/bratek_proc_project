# Generated by Django 4.2.11 on 2024-05-12 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_task_testcase_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='join_code_for_instructor',
            field=models.CharField(default='4', max_length=12, unique=True, verbose_name='Join code for instructor'),
            preserve_default=False,
        ),
    ]