# Generated by Django 2.2.3 on 2019-07-27 06:21

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_publication_starred'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
                ('mediafile', models.FileField(upload_to=core.models.create_filename)),
            ],
        ),
        migrations.RemoveField(
            model_name='publication',
            name='abstract',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='doi',
        ),
    ]
