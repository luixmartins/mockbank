# Generated by Django 5.0.1 on 2024-02-02 00:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_usermessages'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessages',
            name='response_from',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='user.usermessages'),
        ),
    ]
