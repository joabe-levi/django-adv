from django.urls import path
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', views.home, name="home"),
    path('logout/', views.my_logout, name="logout"),
    path('home2/', views.TemplateView.as_view(template_name='home2.html')),
    path('home3/', views.HomePage.as_view(), name='home3'),
    path('view/', views.MyView.as_view())
]