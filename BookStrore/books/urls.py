from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', views.login_page, name='login'),
    path("register/",views.register,name="register"),
    path('logout/', views.log_out, name='logout'),
    path('home/',login_required(views.home),name='home'),
    path('details/<slug:slug>/', views.details, name='details'),
    path('profile/<slug:slug>/', views.profile, name='profile'),
    path("update_profile/<int:id>/", views.update_profile, name="update_profile"),
    path('category_books/<slug:category_slug>/', views.category_books, name='category_books'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart,name="cart"),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('change_password/<token>/',views.change_password,name='change_password'),
]