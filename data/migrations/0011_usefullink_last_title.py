# Generated by Django 5.0.6 on 2024-12-25 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_publications'),
    ]

    operations = [
        migrations.AddField(
            model_name='usefullink',
            name='last_title',
            field=models.CharField(default=2, max_length=150),
            preserve_default=False,
        ),
    ]
