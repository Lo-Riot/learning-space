# Generated by Django 4.1.3 on 2023-02-08 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_courses'),
        ('courses', '0003_rename_creator_course_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='account.author'),
        ),
    ]
