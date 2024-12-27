# Generated by Django 5.0.6 on 2024-12-27 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_usefullink_last_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='words',
            name='comment',
            field=models.TextField(default=2, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='words',
            name='grammatical_description',
            field=models.TextField(default=2, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='words',
            name='lexical_form',
            field=models.TextField(default=2, max_length=1000),
            preserve_default=False,
        ),
    ]