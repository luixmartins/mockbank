# Generated by Django 5.0.1 on 2024-02-02 00:32

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_account_balance_user_account_limit'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessages',
            fields=[
                ('message_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=100)),
                ('message_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message_read', models.BooleanField(default=False)),
                ('message_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_from', to='user.user')),
                ('message_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_to', to='user.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]