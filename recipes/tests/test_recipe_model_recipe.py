from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeModelTest(RecipeTestBase):

    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()  
    
    def make_recipe_to_test_default_fields(self):
        recipe = Recipe(
            title = 'Chocolate com Whey',
            description = 'Uma otima sobremesa para depois do treino',
            slug = 'chocolate-com-whey-1',
            preparation_time = 20,
            preparation_time_unit = 'min',
            servings = 2,
            servings_unit = 'pessoas',
            preparation_steps = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nihil sane. Qui est in parvis malis.',
            category = self.make_category(name='CategoryForTest1'),
            author = self.make_author(username='fehFrancoPro'),
        )
        recipe.full_clean()
        recipe.save()
        return recipe
    
    def test_recipe_title_raises_error_if_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 70

        with self.assertRaises(ValidationError) as error:
            self.recipe.full_clean()

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_length(self, field, ml):       
        setattr(self.recipe, field, 'A' * (ml + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()         
    
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_to_test_default_fields()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_to_test_default_fields()
        self.assertFalse(recipe.is_published, msg='field "is_published" is not false')

    def test_recipe_str_representation_is_correct(self):
        self.recipe.title = 'Any title to test recipe category'
        self.recipe.full_clean()
        self.recipe.save()

        self.assertEqual(str(self.recipe), self.recipe.title , 
                         msg='The str representation must to be the ' 
                         'same as the name')