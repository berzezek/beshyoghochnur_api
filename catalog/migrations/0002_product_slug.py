# Generated by Django 5.1 on 2024-09-25 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=1, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]