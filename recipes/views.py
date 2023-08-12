from django.shortcuts import render
from django.http import HttpResponse
from utils.recipes import factory
# Create your views here.

def home(request):
    recipe = [factory.make_recipe() for _ in range(10)]
    context ={
        'page_title': 'home',
        'recipes': recipe,
    }
    return render(request, 'recipes/pages/home.html', context)

def recipes(request, id):

    context ={
        'page_title': 'recipe',
        'recipe': factory.make_recipe(),
        'one_page': True,
    }

    return render(request, 'recipes/pages/recipes_page.html', context)