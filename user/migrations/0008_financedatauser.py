# Generated by Django 5.0.1 on 2024-02-06 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_usermessages_response_from'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinanceDataUser',
            fields=[
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.user')),
                ('dependents', models.IntegerField(blank=True, default=0)),
                ('education', models.IntegerField(choices=[('completa', 1), ('incompleta', 0)], default=0)),
                ('employed', models.IntegerField(choices=[('empregado', 1), ('desempregado', 0)], default=0)),
                ('annual_income', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8)),
                ('score', models.IntegerField(default=500)),
                ('residential_assets', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8)),
                ('commercial_assets', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8)),
                ('luxury_assets', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8)),
                ('bank_assets', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8)),
            ],
        ),
    ]