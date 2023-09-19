from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse
from django.http import Http404

class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'report your username'),
        ('first_name', 'Write your first name here'),
        ('last_name', 'Write your last name here'),
        ('email', 'Report your email'),
        ('password', 'Type your password'),
        ('password2', 'Confirm your password'),
    ])
    def test_fields_placeholder_are_corrects(self, field, placeholder):
        form = RegisterForm()
        _placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(_placeholder, placeholder)

    @parameterized.expand([
        ('username', 'Your username here'),
        ('email', 'email must be valid'),
        ('password2', 'both passwords must be equal'),
    ])
    def test_if_help_text_are_corrects(self, field, ht):
        form = RegisterForm()
        _ht = form[field].help_text
        self.assertEqual(_ht, ht)

    @parameterized.expand([
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Último nome'),
        ('username', 'Digite seu usuario'),
        ('email', 'Endereço de email'),
        ('password', 'Password1'),
        ('password2', 'Password2'),
    ])
    def test_if_labels_are_corrects(self, field, label):
        form = RegisterForm()
        _label = form[field].field.label
        self.assertEqual(_label, label)

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            'first_name': 'first',
            'last_name': 'last',
            'username': 'username1',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }

        return super().setUp()
    
    @parameterized.expand([
        ('username', 'Esse campo é obrigatorio seu arrombado'),
        ('first_name', 'first name must not be empty'),
        ('last_name', 'last name must not be empty'),
        ('email', 'Email must not be empty'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_if_form_field_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
    
    def test_username_field_min_len_is_working(self):
        #min_len = 4
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data,follow=True)
        msg = 'You have not reached the min len of 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_len_is_working(self):
        #min_len = 150
        self.form_data['username'] = 'j' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data,follow=True)
        msg = 'You exceeded the limit of 150 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_if_password_chars_validation_is_working(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data,follow=True)
        msg = (
            'Password must have at least one uppercase and lowercase letter, '
            'one number and the len must be at least 8 characaters'
            )
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))


        self.form_data['password'] = '@A123abc123'
        response = self.client.post(url, data=self.form_data,follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_if_the_both_passwords_are_the_same(self):
        self.form_data['password'] = 'Str0ngP@ssword1'
        self.form_data['password2'] = 'Str0ngP@ssword2'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data,follow=True)
        msg =  'both passwords must be "EQUAL"'
        msg_html = 'both passwords must be &quot;EQUAL&quot;'
        self.assertIn(msg_html, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))


        self.form_data['password'] = 'Str0ngP@ssword2' * 150
        self.form_data['password2'] = 'Str0ngP@ssword2' * 150

        response = self.client.post(url, data=self.form_data,follow=True)

        self.assertNotIn(msg_html, response.content.decode('utf-8'))
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_success_message_show_after_registering_a_user(self):
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data,follow=True)
        msg = 'Your user was save, please log in'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_http404_raises_when_request_for_create_url_is_not_post(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_duplication_email_check(self):
        self.form_data['email'] = 'email1@gmail.com'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data,follow=True)
        self.form_data['email'] = 'email1@gmail.com'
        response = self.client.post(url, data=self.form_data,follow=True)
        msg = 'This email is already in use, use another'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email'))
