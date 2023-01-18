from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.list import ListView

from clientes.models import Person


class HomePage(TemplateView):
    template_name = 'home3.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data()
        context['minha_variavel'] = 'Olá, seja bem vindo'
        return context


def calcular(v1, v2):
    return v1 / v2


def home(request):
    value1 = 10
    value2 = 20
    result = calcular(value1, value2)
    return render(request, 'home/home.html', {'result': result})


class MyView(View):

    def get(self, request, *args, **kwargs):
        response = render_to_response('home3.html')
        response.set_cookie('color', 'blue', max_age=1000)
        return response

    def post(self, request, *args, **kwargs):
        return HttpResponse('post')


def my_logout(request):
    logout(request)
    return redirect('home')


class PersonList(LoginRequiredMixin, ListView):
    model = Person
