from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name='categoriaMinha'):
        return Category.objects.create(name=name)
    
    def make_author(
            self, 
            first_name='Kleber',
            last_name='Bambam',
            username='klebaoBirrll',
            password='123456',
            email='user@email.com'):
        
        return User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
            self,
            title = 'Chocolate com Whey',
            description = 'Uma otima sobremesa para depois do treino',
            slug = 'chocolate-com-whey',
            preparation_time = 20,
            preparation_time_unit = 'min',
            servings = 2,
            servings_unit = 'pessoas',
            preparation_steps = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nihil sane. Qui est in parvis malis.',
            preparation_steps_is_html = False,
            is_published = True,
            category_data = None,
            author_data = None
    ):
        
        if category_data is None:
            category_data = {}
        
        if author_data is None:
            author_data = {}


        return Recipe.objects.create(
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            servings_unit = servings_unit,
            preparation_steps = preparation_steps,
            preparation_steps_is_html = preparation_steps_is_html,
            is_published = is_published,
            category = self.make_category(**category_data),
            author = self.make_author(**author_data),
        )
        
