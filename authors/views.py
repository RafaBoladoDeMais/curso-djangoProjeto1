from django.shortcuts import render, redirect
from django.http import Http404
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse


# Create your views here.

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)
    form_action = reverse('authors:create')
    return render(request, 'authors/pages/register_view.html',{
        'form': form,
        'page_title': 'Cadastre-se',
        'form_action': form_action,
    })

def register_created(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user: User = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user was save, please log in')
        del(request.session['register_form_data'])
    
    return redirect('authors:register')