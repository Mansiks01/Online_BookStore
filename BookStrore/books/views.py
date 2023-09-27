from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Category, Book,Profile,Cart, Cartitems
from django.core.paginator import Paginator
from django.http import JsonResponse
import uuid
from .helpers import send_forget_password_mail
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta
import mysql.connector
import re

path = 'my.cnf'
# Create your views here.
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials')
            return redirect('/')
        else:
            login(request, user)

            if remember_me:
                response = redirect('/home/')
                response.set_signed_cookie('remembered_username', username)
                response.set_signed_cookie('remembered_password', password)
                return response

            return redirect('/home/')
    else:        
        remembered_username = request.get_signed_cookie('remembered_username', default=None)
        remembered_password = request.get_signed_cookie('remembered_password', default=None)

        if remembered_username and remembered_password:
            user = authenticate(username=remembered_username, password=remembered_password)
            if user:
                login(request, user)
                return redirect('/home/')

    # If neither POST nor remembered cookies, show the login page
    return render(request, 'books/login.html')



def log_out(request):
    logout(request)

    response = redirect('/')
    response.delete_cookie('remembered_username')
    response.delete_cookie('remembered_password')
    
    return response
    

def register(request):
    if request.method == "POST" :
        username = request.POST.get('user_name')
        email = request.POST.get('email')
        password= request.POST.get('password')
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        password_pattern = r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,20}$'
        user= User.objects.filter(username=username)
        if user:            
            messages.error(request,"username already exists")
            return redirect('/register/')
        elif User.objects.filter(email = email):
            messages.error(request,'Already have a account with this e-mail')
        elif len(username)<2 or len(email)<3 :
            messages.error(request, "Username too small")
        elif not re.match(email_pattern, email):
            messages.error(request, "email not correct") 
  
        elif not re.match(password_pattern, password):
            messages.error(request, "Password pattern is not correct")   
        else:        

            user = User.objects.create(username=username,email=email,last_name=last_name,first_name=first_name)
            user.set_password(password)
            user.save()
            messages.error(request,"Account created succesfully")
            return redirect('/register/')
    return render(request,'books/register.html')

@login_required(login_url='/')
def home(request):
    categories = Category.objects.all()
    books_by_category = {}
    
    

    for category in categories:
        books = Book.objects.filter(category=category)[:4]
        books_by_category[category] = books
    
    return render(request, 'books/home.html', {'books_by_category': books_by_category})

def details(request, slug):
    # Use get_object_or_404 to retrieve the book object by slug or return a 404 page if not found
    book = get_object_or_404(Book, slug=slug)

    return render(request, 'books/details.html', {'book': book})


def profile(request, slug):
    profile_detail = None  
    
    try:
        connection = mysql.connector.connect(option_files=path)
        if connection.is_connected():
            cursor = connection.cursor()
            query = f"select * from auth_user where username = %s;"
            cursor.execute(query, (slug,))
            profile_detail = cursor.fetchall()
            
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return render(request, 'books/profile.html', {'profile_detail': profile_detail})


def update_profile(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
            username = request.POST.get('user_name')
            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')
            email = request.POST.get('email')
            image = request.FILES.get('image')

            # Update user fields
            if username:
                user.username = username
            if firstname:
                user.first_name = firstname
            if lastname:
                user.last_name = lastname
            if email:    
                user.email = email
            if image:
                user.image = image

            user.save()
            print("Changes saved")
            slug = User.objects.filter(id=id).values('username').first()
            if slug:
                username_str = slug['username']

            return redirect('profile', slug=username_str)
            
    

    context = {'user': user}  # Pass the user object to the template
    return render(request, 'books/update.html', context)


def category_books(request, category_slug):
    category = Category.objects.get(genre=category_slug)
    all_books = Book.objects.filter(category=category)

    paginator = Paginator(all_books,2)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    return render(request, 'books/category_books.html', {'category': category, 'books': books})



# views.py
from django.http import JsonResponse

def add_to_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided

        # Get the book and user
        book = Book.objects.get(id=book_id)
        user = request.user

        # Check if a cart for the user exists, if not, create one
        cart, created = Cart.objects.get_or_create(user=user, is_paid=False)

        if action == 'plus':
            # Check if the book is already in the cart
            cart_item, created = Cartitems.objects.get_or_create(cart=cart, product=book)
            
            # Update the quantity of the book in the cart
            cart_item.quantity += quantity
            cart_item.save()
        elif action == 'minus':
            # Get the cart item for the book
            cart_item = Cartitems.objects.get(cart=cart, product=book)
            
            # Reduce the quantity if it's greater than 0
            if cart_item.quantity > 0:
                cart_item.quantity -= quantity
                cart_item.save()
        
        return JsonResponse({'message': 'Book added to cart successfully'})

    return JsonResponse({'message': 'Invalid request'}, status=400)

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def change_password(request,token):
    context ={}
    password_pattern = r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,20}$'
    profile_obj = Profile.objects.filter(forget_password_token =token ).first()
    context = {'user_id':profile_obj.user.id}
    print(request.method)
    if request.method == 'POST':
        if profile_obj.token_expiration_time >= timezone.now():
            # if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                user_id  = request.POST.get('user_id')

                if user_id is None :
                    messages.error(request,'No user found')
                    return redirect(f'/change_password/{token}/')

                if new_password != confirm_password:
                    messages.error(request,'Password does not match')
                    return redirect(f'/change_password/{token}/')
                elif not re.match(password_pattern, new_password):
                    messages.error(request, "Password pattern is not correct")  
                
                user_obj = User.objects.get(id = user_id)
                user_obj.set_password(new_password)
                user_obj.save()
                profile_obj.forget_password_token = None 
                profile_obj.token_expiration_time = None
                profile_obj.save()
                return redirect('/login/')
        else:
                messages.error(request, 'The password reset link has expired.')
                return redirect('/forget_password/')

       
    return render(request,'books/change_password.html',context)



def forget_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.error(request, 'User not found')
                return redirect('/forget_password/')
            
            
            user_obj = User.objects.get(username=username)
            
            
            profile_obj = Profile.objects.get(user=user_obj)
           
            token = str(uuid.uuid4())
            profile_obj.forget_password_token = token
            profile_obj.token_expiration_time = timezone.now() + timedelta(minutes=5)
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'Email is sent to your email id')
            return redirect('/forget_password/')

    except Exception as e:
        print(e)    
    return render(request, 'books/forget_password.html')


def cart(request):
     
    user = request.user
    cart_items = Cartitems.objects.filter(cart__is_paid = False,cart__user = user) 

       
    # details = Book.objects.filter(title=cart_items)
    return render(request,'books/cart.html',{'cart_items':cart_items})