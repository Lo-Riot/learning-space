# Generated by Django 4.1.3 on 2023-03-19 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_rename_courses_user_enrollments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='enrollments',
        ),
    ]