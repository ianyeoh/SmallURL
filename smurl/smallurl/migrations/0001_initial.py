# Generated by Django 4.1.6 on 2023-02-03 04:18

from django.db import migrations, models
import smallurl.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.CharField(default=smallurl.models.idgen, max_length=5, primary_key=True, serialize=False)),
                ('original_url', models.URLField()),
            ],
        ),
    ]
