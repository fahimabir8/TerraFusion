# Generated by Django 5.0.6 on 2024-10-01 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_account_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
