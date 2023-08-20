from .test_recipe_base import RecipeTestBase, Category
from django.core.exceptions import ValidationError
from parameterized import parameterized

class CategoryModelTest(RecipeTestBase):

    def setUp(self):
        self.category = self.make_category(
            name='Any title to test model category'
        )
        return super().setUp()  
    
    def test_category_str_representation_is_correct(self):
        correct_str = str(self.category)
        self.assertEqual(correct_str, self.category.name, 
                         msg='The str representation must to be '
                         f'{self.category.name} but {correct_str} is defined')
        
    def test_recipe_title_raises_error_if_has_more_than_65_chars(self):
        self.category.name = 'A' * 66

        with self.assertRaises(ValidationError):
            self.category.full_clean()
