# Generated by Django 4.2.9 on 2024-01-05 18:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analyser", "0002_rename_name_videorecord_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="Creator",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name="videorecord",
            name="creator",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="analyser.creator"),
        ),
    ]
