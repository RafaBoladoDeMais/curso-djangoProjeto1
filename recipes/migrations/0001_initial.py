# Generated by Django 4.2.4 on 2023-08-12 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updatad_at', models.DateTimeField(auto_created=True)),
                ('title', models.CharField(max_length=65)),
                ('decription', models.CharField(max_length=165)),
                ('slug', models.SlugField()),
                ('preparation_time', models.CharField(max_length=65)),
                ('preparation_time_unit', models.IntegerField()),
                ('servings', models.CharField(max_length=65)),
                ('servings_unit', models.IntegerField()),
                ('prepartaion_steps', models.TextField()),
                ('prepartaion_steps_is_html', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=False)),
                ('cover', models.ImageField(upload_to='recipes/covers/%Y/%m/%d')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
            },
        ),
    ]