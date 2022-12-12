# Generated by Django 4.1.3 on 2022-12-12 18:50

import core.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_profile_first_name_alter_profile_last_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name_plural': 'Users'},
        ),
        migrations.AlterModelOptions(
            name='postmaker',
            options={'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(2), core.validators.validate_letters]),
        ),
    ]