from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeHomeViewsTests(RecipeTestBase):

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


class RecipeCategoryViewsTests(RecipeTestBase):
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


class RecipePageViewsTests(RecipeTestBase):
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
