# Generated by Django 4.1.3 on 2023-02-14 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='video',
            field=models.FileField(null=True, upload_to='uploads/'),
        ),
    ]
