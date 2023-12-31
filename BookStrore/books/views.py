import re
import uuid
import mysql.connector
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum,F
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .helpers import send_forget_password_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Category, Book,Profile,Cart, Cartitems
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render ,redirect,get_object_or_404

path = 'my.cnf'
# Create your views here.


#User Login related details
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
    try: 
        if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            password_pattern = r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,20}$'
            
            # Check if a user with the same username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('/register/')
            
            # Check if a user with the same email already exists
            elif username is None:
                messages.error(request, "Username is missing")

            elif first_name is None:
                messages.error(request, "first name is missing")
                 
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Account with this email already exists')
            
            # Check for minimum length requirements for username and email
            elif len(username) < 2 or len(email) < 3:
                messages.error(request, "Username or email is too short")
            
            # Check if the email format is correct
            elif not re.match(email_pattern, email):
                messages.error(request, "Email is not in a valid format")
            
            # Check if the password meets the pattern requirements
            elif not re.match(password_pattern, password):
                messages.error(request, "Password does not meet requirements")
            
            else:
                # Create a new user
                user = User.objects.create(username=username, email=email, last_name=last_name, first_name=first_name)
                user.set_password(password)
                user.save()
                messages.success(request, "Account created successfully")
                return redirect('/register/')
    except Exception as e:
        messages.error(request, "Something went wrong")
        print(e)
    
    return render(request, 'books/register.html')


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
                return redirect('/')
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
        messages.success(request, e)   
    return render(request, 'books/forget_password.html')








#home page and related functions
@login_required(login_url='/')
def home(request):
    categories = Category.objects.all()
    books_by_category = {}
    book_found = False  # Add a flag to track if any book was found

    # Get the search query from the request
    search = request.GET.get('search')

    # Get the sorting and ordering parameters from the request
    sort_by = request.GET.get('sort_by')
    order_by = request.GET.get('order_by')

    for category in categories:
        books = Book.objects.filter(category=category)

        # Apply filtering based on the search query
        if search:
            books = books.filter(Q(title__icontains=search) | Q(author__icontains=search))
            if books.exists():
                book_found = True  # Set the flag to True if books are found
            else:
                continue  # No books found in this category, move to the next

        # Apply sorting and ordering
        if sort_by:
            if order_by == 'asc':
                books = books.order_by(sort_by)
            elif order_by == 'desc':
                books = books.order_by(f'-{sort_by}')

        # Store the filtered and sorted books in the dictionary
        books_by_category[category] = books[:4]

    # Check if any book was found and display a message accordingly
    if search and not book_found:
        messages.success(request, 'Book not found')

    return render(request, 'books/home.html', {'books_by_category': books_by_category})



def details(request, slug):
    # Use get_object_or_404 to retrieve the book object by slug or return a 404 page if not found
    book = get_object_or_404(Book, slug=slug)

    return render(request, 'books/details.html', {'book': book})

def category_books(request, category_slug):
    category = Category.objects.get(genre=category_slug)
    all_books = Book.objects.filter(category=category)

    paginator = Paginator(all_books,4)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    return render(request, 'books/category_books.html', {'category': category, 'books': books})








#User related functions
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







#cart related functions
def add_to_cart(request, id):
    try : 
        book = get_object_or_404(Book, id=id)
        quantity = int(request.POST.get('quantity', 1))     
        cart, user_created = Cart.objects.get_or_create(user=request.user)    
        cart_item, created = Cartitems.objects.get_or_create(cart=cart, product=book)        
        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity <= book.available_quantity:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, f'Added {quantity} item(s) of {book.title} to your cart.')

            else:
                messages.warning(request, "Quantity exceeds available book quantity.")                

        else:
            cart_item.quantity = quantity
        if cart_item.quantity < 0 :
            messages.success(request, "Add correct quantity")                
    except Exception as e :
             messages.success(request, "Add correct quantity")   
             print(e) 
    # cart_item.save()
    
    return redirect('cart')


def cart(request): 
    
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = Cartitems.objects.filter(cart__is_paid = False,cart__user = user) 
    total_price = cart_items.aggregate(total_price=Sum(F('product__price') * F('quantity')))['total_price']
    try: 
        if request.method == 'POST':            
                    # Update cart items, set is_paid to True
                    cart.is_paid=True
                    # Decrease the available quantity of books
                    for cart_item in cart_items:
                        book = cart_item.product
                        quantity = cart_item.quantity
                        book.available_quantity -= quantity
                        book.save()
                # Clear the cart
                    cart_items.delete()

                    messages.success(request, 'Payment successful. Your order has been placed.')
                    return redirect('/home/')
    except Exception as e :
         messages.success(request,"Something went wrong, try to reduce quantity of book")   
    
    return render(request,'books/cart.html',{'cart_items':cart_items,'total_price': total_price})


def remove_cart(request, cart_item_id):
    try : 
        cart_item = Cartitems.objects.get(id = cart_item_id)
        cart_item.delete()

    except Exception as e:
        print(e)    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def make_payment(request):    
        try:
            user = request.user
            cart_items = Cartitems.objects.filter(cart__is_paid=False, cart__user=user)
    # total_price = cart_items.aggregate(total_price=Sum('product__price'))['total_price']

            if request.method == 'POST':
            
                # Update cart items, set is_paid to True
                cart_items.update(cart__is_paid=True)

                # Decrease the available quantity of books
                for cart_item in cart_items:
                    book = cart_item.product
                    book.available_quantity -= cart_item.quantity
                    book.save()

            # Clear the cart
                cart_items.delete()

                messages.success(request, 'Payment successful. Your order has been placed.')
                return redirect('/home/')

        except Exception as e:
            messages.error(request, 'Payment failed. Please try again.')
            return HttpResponse('Error')


