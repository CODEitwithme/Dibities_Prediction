from django.urls import path
from home import views
from .views import prediction, savedmodel  # Import views from views.py



urlpatterns = [
    path('index', views.index, name='home'),
    path('about', views.about, name='about'),
    path('prediction', views.prediction, name='prediction'),
    path('contact', views.contact, name='contact'),
    path('home', views.index, name='home'),
    path('prediction/', prediction, name='prediction'),
    path('result/', views.result, name='result'),
    path('', views.login, name='login')
]