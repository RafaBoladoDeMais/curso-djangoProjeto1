from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views

 
class RecipeViewsTests(TestCase):
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
    def test_recipe_home_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_page_return_404_if_recipe_not_found(self):
        response = self.client.get(reverse('recipes:recipe', args=(2, )))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_return_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', args=(2, )))
        self.assertEqual(response.status_code, 404)


    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', args=(1, )))
        self.assertIs(view.func, views.category)

    def test_recipe_page_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=(1, )))
        self.assertIs(view.func, views.recipes)
    
