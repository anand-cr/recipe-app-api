# Generated by Django 4.2 on 2023-04-10 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_tag_recipe_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
    ]
