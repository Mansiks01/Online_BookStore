from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



# class CustomUser(AbstractUser):
#     profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

# Category model for book genres
class Category(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre

# Book model for book details
class Book(models.Model):    
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available_quantity = models.PositiveIntegerField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)  
    description = models.TextField(blank=True, null=True) 
    book_image = models.ImageField(upload_to='Book_image/', null=True, blank=True)

    def __str__(self):
        return self.title

# Cart model for user shopping carts
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)

# Cartitems model for items within a user's shopping cart
class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.product)

# Profile model for user profiles
class Profile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token_expiration_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
