# Generated by Django 4.2.4 on 2023-08-13 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_category_recipe_author_recipe_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='prepartaion_steps',
            new_name='preparation_steps',
        ),
    ]
