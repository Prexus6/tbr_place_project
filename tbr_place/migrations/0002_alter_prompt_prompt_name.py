# Generated by Django 5.0.6 on 2024-07-07 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tbr_place", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prompt",
            name="prompt_name",
            field=models.TextField(verbose_name=250),
        ),
    ]
