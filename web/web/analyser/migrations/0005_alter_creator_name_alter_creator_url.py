# Generated by Django 4.2.9 on 2024-01-05 18:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analyser", "0004_creator_url_alter_videorecord_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creator",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="creator",
            name="url",
            field=models.URLField(blank=True, null=True, unique=True),
        ),
    ]
