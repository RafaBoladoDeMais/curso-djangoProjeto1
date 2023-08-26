from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404, HttpResponse
from . import models
from django.db.models import Q
from utils.pagination_func import make_pagination_range, make_pagination


PER_PAGE = 9

def home(request):
    recipes = models.Recipe.objects.all().filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context ={
        'page_title': 'Home',
        'recipes': page_obj,
        'pagination_range': pagination_range
    }
    return render(request, 'recipes/pages/home.html', context)


def recipes(request, id):
    recipe = models.Recipe.objects.filter(id=id).first()
    recipe = get_object_or_404(models.Recipe.objects.filter(id=id, is_published=True))
    page_title = f'Receita - {recipe.title}' #type: ignore 

    context ={
        'page_title': page_title,
        'recipe': recipe,
        'one_page': True,
    }

    return render(request, 'recipes/pages/recipes_page.html', context)

def category(request, id):
    # recipe = models.Recipe.objects.filter(category__id=id, is_published=True)
    # if not recipe:
    #     raise Http404('Not found 🙁')
    recipe = get_list_or_404(
        models.Recipe.objects.filter(
        category__id=id, 
        is_published=True).order_by('-id'),
    )
    page_obj, pagination_range = make_pagination(request, recipe, PER_PAGE)
    
    page_title = f'Categorias - {recipe[0].category.name}'#type: ignore 
    context ={
        'page_title': page_title,
        'recipes': page_obj,
        'pagination_range': pagination_range,

    }

    return render(request, 'recipes/pages/home.html', context)

def search(request):
    search_term = request.GET.get('q', '').strip()

        
    if not search_term:
        raise Http404 
    page_title = f'Search for "{search_term}"'
    recipes = models.Recipe.objects.filter(
        Q(        
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(author__first_name__icontains=search_term) |
            Q(author__last_name__icontains=search_term) |
            Q(category__name__icontains=search_term)
        ),
        is_published=True

    ).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context ={
        'page_title': page_title,
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
    }
    return render(request,'recipes/pages/search.html', context)

