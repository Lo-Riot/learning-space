# Generated by Django 4.1.3 on 2023-02-02 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_rename_creator_course_author'),
        ('account', '0002_rename_creator_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(to='courses.course'),
        ),
    ]