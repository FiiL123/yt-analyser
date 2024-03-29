# Generated by Django 4.2.9 on 2024-01-06 08:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analyser", "0009_alter_creator_times_watched"),
    ]

    operations = [
        migrations.AddField(
            model_name="videorecord",
            name="categories",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="videorecord",
            name="duration",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="videorecord",
            name="tags",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
