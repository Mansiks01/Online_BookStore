from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required




urlpatterns = [
    path('', views.login_page, name='login'),
    path("register/",views.register,name="register"),
    path('logout/', views.log_out, name='logout'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('change_password/<token>/',views.change_password,name='change_password'),

    path('home/',login_required(views.home),name='home'),
    path('details/<slug:slug>/', views.details, name='details'),
    path('category_books/<slug:category_slug>/', views.category_books, name='category_books'),

    path('profile/<slug:slug>/', views.profile, name='profile'),
    path("update_profile/<int:id>/", views.update_profile, name="update_profile"),
    
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart,name="cart"),
    path('remove_cart/<int:cart_item_id>',views.remove_cart,name='remove_cart'),
    
]
