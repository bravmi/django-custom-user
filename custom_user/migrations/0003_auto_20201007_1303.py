# Generated by Django 3.1.2 on 2020-10-07 13:03

import custom_user.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0002_auto_20201005_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True, validators=[custom_user.validators.UsernameValidator()]),
        ),
    ]
