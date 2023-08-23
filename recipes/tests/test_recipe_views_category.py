from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewsTest(RecipeTestBase):
    def test_recipe_category_templates_loads_recipes(self):
        #TESTANDO CATEGORY
        nedded_title = 'This is the category test'

        self.make_recipe(
            title=nedded_title, 
            category_data={
                'name':'Chocolate category',
                }
            )

        response = self.client.get(reverse('recipes:category', args=(1, )))
        content = response.content.decode('utf-8')
 
        self.assertIn(nedded_title, content)
        self.assertIn('Chocolate category', content)

    def test_recipe_category_return_404_if_no_recipes_in_this_one(self):
        response = self.client.get(reverse('recipes:category', args=(1000, )))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_function_is_correct(self): 
        view = resolve(reverse('recipes:category', args=(1, )))
        self.assertIs(view.func, views.category)

    def test_recipe_category_template_dont_loads_recipes_if_its_not_published(self):
        self.make_recipe(
            is_published=False
        )
        response = self.client.get(reverse('recipes:category', args=(1, )))
        self.assertEqual(response.status_code, 404)


