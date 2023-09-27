from django.db import models
from django.contrib.auth.models import User

 

class Category(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre

class Book(models.Model):    
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available_quantity = models.PositiveIntegerField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)  
    description = models.TextField(blank=True, null=True) 
    

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    
    # def get_cart_count(self):
    #     return Cartitems.objects.filter(Cart__is_paid = False,Cart__user = self.user).count()
    
    def __str__(self):
        return str(self.user)

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart")
    product = models.ForeignKey(Book,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return str(self.product)

    


    
class Profile(models.Model) :
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token_expiration_time = models.DateTimeField(null=True, blank=True)

    

    def __str__(self):
        return self.user.username
