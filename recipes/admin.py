from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = 'id', 'title',

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',