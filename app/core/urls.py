from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.authentication_page, name='auth'),
    path('logout/', views.logout_page, name='logout'),
]
