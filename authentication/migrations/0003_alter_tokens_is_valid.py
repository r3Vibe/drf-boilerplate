# Generated by Django 5.0 on 2023-12-09 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_tokens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokens',
            name='is_valid',
            field=models.BooleanField(default=False),
        ),
    ]
