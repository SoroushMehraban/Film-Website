from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.authentication_page, name='auth'),
    path('comment/<int:movie_id>', views.comment_page, name='comment'),
    path('logout/', views.logout_page, name='logout'),
]
