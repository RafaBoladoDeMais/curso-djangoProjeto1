from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipePageViewsTest(RecipeTestBase):
    def test_recipe_page_templates_loads_recipes(self):
        #TESTANDO RECIPE PAGE
        nedded_title = 'This is the recipe page test'

        self.make_recipe(
            title=nedded_title, 
            author_data={
                'first_name':'Neymar',
                'last_name': 'Jr',
                }
            )

        response = self.client.get(reverse('recipes:recipe', args=(1, )))
        content = response.content.decode('utf-8')
 
        self.assertIn(nedded_title, content) 
        self.assertIn('Neymar Jr', content)        

    def test_recipe_page_return_404_if_recipe_not_found(self):
        response = self.client.get(reverse('recipes:recipe', args=(1000, )))
        self.assertEqual(response.status_code, 404)

    def test_recipe_page_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=(1, )))
        self.assertIs(view.func, views.recipes)

    def test_recipe_page_template_dont_loads_recipe_if_its_not_published(self):
        self.make_recipe(
            is_published=False
        )
        response = self.client.get(reverse('recipes:recipe', args=(1, )))
        self.assertEqual(response.status_code, 404)


