# Generated by Django 4.1.6 on 2023-02-05 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smallurl', '0004_alter_url_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='expire_time',
            field=models.DateTimeField(null=True),
        ),
    ]
