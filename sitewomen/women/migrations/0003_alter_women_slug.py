# Generated by Django 4.2.1 on 2023-10-23 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("women", "0002_alter_women_options_women_slug_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="women",
            name="slug",
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
