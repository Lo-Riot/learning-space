# Generated by Django 4.1.3 on 2023-02-09 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_courses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='courses',
            new_name='enrollments',
        ),
    ]
