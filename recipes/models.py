from django.db import models

# Create your models here.
class Recipe(models.Model):
    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    title = models.CharField(max_length=65)
    decription = models.CharField(max_length=165)
    slug = models.SlugField()
    preparation_time = models.CharField(max_length=65)
    preparation_time_unit = models.IntegerField()
    servings = models.CharField(max_length=65)
    servings_unit = models.IntegerField()
    prepartaion_steps = models.TextField()
    prepartaion_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updatad_at = models.DateTimeField(auto_created=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d')

    
    def __str__(self):
        return self.title