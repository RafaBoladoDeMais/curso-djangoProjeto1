from unittest import TestCase
from recipes.tests.test_recipe_base import RecipeTestBase
from utils.pagination_func import make_pagination_range
from django.urls import reverse, resolve
from unittest.mock import patch

class PaginationTest(RecipeTestBase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination'] 

        self.assertEqual([1, 2, 3, 4], pagination)
    
    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        
        #current_page = 1; expected_range = [1, 2, 3, 4]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)


        #current_page = 2; expected_range = [1, 2, 3, 4]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination'] 

        self.assertEqual([1, 2, 3, 4], pagination)


        #current_page = 3; expected_range = [2, 3, 4, 5]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination'] 

        self.assertEqual([2, 3, 4, 5], pagination)


        #current_page = 4; expected_range = [3, 4, 5, 6]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination'] 

        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        
        #current_page = 10; expected_range = [9, 10, 11, 12]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination'] 

        self.assertEqual([9, 10, 11, 12], pagination)


        #current_page = 12; expected_range = [11, 12, 13, 14]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination'] 

        self.assertEqual([11, 12, 13, 14], pagination)

    def test_pagination_range_stay_static_if_its_in_the_final_range(self):
        #current_page = 18; expected_range = [17, 18, 19, 20]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination'] 

        self.assertEqual([17, 18, 19, 20], pagination)

        #current_page = 19; expected_range = [17, 18, 19, 20]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination'] 

        self.assertEqual([17, 18, 19, 20], pagination)

        #current_page = 20; expected_range = [17, 18, 19, 20]
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=22,
        )['pagination'] 

        self.assertEqual([17, 18, 19, 20], pagination)
    
    #CP is current page  ->
    def test_pagination_raises_value_error_if_type_of_cp_arg_is_not_int(self):
        url = reverse('recipes:home')
        for i in range(10):
            self.make_recipe(
                slug=f'slug-{i}',
                author_data={
                'username': f'user{i}'}
            )
        page_num_for_test = 2
        response1 = self.client.get(url + f'?page=a')
        response2 = self.client.get(url + f'?page={page_num_for_test}')
        
        self.assertEqual(1, response1.context['pagination_range']['current_page'])
        self.assertEqual(2, response2.context['pagination_range']['current_page'])

    def test_pagination_loads_recipes(self):
        url = reverse('recipes:home')
        for i in range(10):
            self.make_recipe(
                slug=f'slug-{i}',
                author_data={
                'username': f'user{i}'},
                title=f'title test {i}'
            )
        page_num = 1
        response = self.client.get(url + f'?page={page_num}')

        self.assertIn('title test 2', response.content.decode('utf-8'))

    def test_recipe_home_is_paginated(self):

        for i in range(17):
            kwargs = {'slug': f'r-{i}', 'author_data':{'username': f'user{i}'}}
            self.make_recipe(**kwargs)


        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 6)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(4)), 3)
        self.assertEqual(len(paginator.get_page(6)), 2)
        