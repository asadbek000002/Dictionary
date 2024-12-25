# Generated by Django 5.0.6 on 2024-12-24 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_text_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=13)),
                ('message', models.TextField(max_length=10000)),
            ],
        ),
    ]