# Generated by Django 5.0.6 on 2024-12-24 17:03
from django.utils.timezone import now
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=now),
            preserve_default=False,
        ),
    ]
