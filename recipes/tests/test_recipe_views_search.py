from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeSearchViewTests(RecipeTestBase):
    def test_recipe_search_uses_correct_view(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)  
        pass

    
    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_args(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_and_is_escaped(self):
        url = reverse('recipes:search')
        response = self.client.get(url + '?q=<Teste>')
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )
    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_can_find_recipe_by_first_name(self):
        first_name1 = 'miranha_peter'
        first_name2 = 'miranha_venom'

        recipe1 = self.make_recipe(
            slug='one', author_data={'first_name': first_name1, 'username':'one'}
        )
        recipe2 = self.make_recipe(
            slug='one', author_data={'first_name': first_name2, 'username':'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={first_name1}')
        response2 = self.client.get(f'{search_url}?q={first_name2}')
        response_both = self.client.get(f'{search_url}?q=miranha')

        expected1 = recipe1.author.first_name #type:ignore
        expected2 = recipe2.author.first_name #type:ignore
        what_is_there1 = response1.content.decode('utf-8')
        what_is_there2 = response2.content.decode('utf-8')

        self.assertIn(expected1, what_is_there1)
        self.assertNotIn(expected2, what_is_there1)

        self.assertIn(expected2, what_is_there2)
        self.assertNotIn(expected1, what_is_there2)

        self.assertIn(expected1, response_both.content.decode('utf-8'))
        self.assertIn(expected2, response_both.content.decode('utf-8'))
