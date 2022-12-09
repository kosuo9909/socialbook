# Generated by Django 4.1.3 on 2022-12-09 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_profile_id_remove_profile_id_user_profile_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileimg',
            field=models.ImageField(blank=True, default='defaults/def.png', null=True, upload_to='profile_images', verbose_name='Profile Picture'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='timeline',
            field=models.ImageField(blank=True, default='defaults/timeline.png', null=True, upload_to='timeline_images', verbose_name='Timeline Picture'),
        ),
    ]
