# Generated by Django 3.2.6 on 2021-08-13 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="name",
            field=models.CharField(default="Stephen King", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="library.author",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="book",
            name="title",
            field=models.CharField(default="The Shining", max_length=100),
            preserve_default=False,
        ),
    ]
