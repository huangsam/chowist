# Generated by Django 3.0.8 on 2020-07-12 17:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("places", "0010_auto_20200712_0505"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["name"], "verbose_name_plural": "categories"},
        ),
        migrations.AlterModelOptions(
            name="review",
            options={"ordering": ["rating"]},
        ),
    ]
