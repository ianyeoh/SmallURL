# Generated by Django 4.1.6 on 2023-02-03 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smallurl', '0003_url_tls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
