from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = 'id', 'title',
    list_display_links = 'id', 'title', 

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'id', 'name', 