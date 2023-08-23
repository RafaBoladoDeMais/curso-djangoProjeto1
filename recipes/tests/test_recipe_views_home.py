from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeHomeViewsTest(RecipeTestBase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipe_found_if_no_recipes(self):

        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>Nao há receitas para mostrar😢</h1>',
            response.content.decode('utf-8')
        )
    
    def test_recipe_home_template_dont_loads_recipes_if_its_not_published(self):
        self.make_recipe(
            is_published=False
        )
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>Nao há receitas para mostrar😢</h1>',
            response.content.decode('utf-8')
        )


    def test_recipe_home_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home')) 
        self.assertEqual(response.status_code, 200)
    

    def test_recipe_home_templates_loads_recipes(self):
        #TESTANDO HOME
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
 
        self.assertIn('Chocolate com Whey', content)
        self.assertIn('20 min', content)        
        self.assertEqual(len(response.context['recipes']), 1)


        # response_recipes = response.context['recipes'].first()

        # self.assertEqual(response_recipes.title, 'Chocolate com Whey')
        # self.assertEqual(response_recipes.author, author)


