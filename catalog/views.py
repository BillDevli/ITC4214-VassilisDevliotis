from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ProductForm
from django import forms
import json
from cart.cart import Cart

from django.contrib.auth.decorators import login_required


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Your Info Has Been Updated!")
            return redirect('home')
        return render(request, "catalog/update_info.html", {'form':form})
            
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password Updated.")
                login(request, current_user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'catalog/update_password.html', {'form':form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Profile Updated!")
            return redirect('home')
        return render(request, 'catalog/update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')

def home(request):

    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products':products})

def category(request,cat):
    cat = cat.replace('-', ' ')
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'catalog/category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("Category does not exist"))
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            return redirect('home')
        else:
            messages.success(request, ("Not correct USERNAME or PASSWORD. Try again."))
            return redirect('login')

    else:
        return render(request, 'catalog/login.html', {})    

def logout_user(request):
    logout(request)
    messages.success(request, ("You Logged out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registered Successful. Fill out Billing Info"))
            return redirect('update_info')
        else:
            messages.success(request, ("Registered not Successful"))
            return redirect('register')
    else:
        return render(request, 'catalog/register.html', {'form':form})
    

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'catalog/product.html', {'product':product})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('home')
        else:
            messages.error(request, "Error adding product. Please check the form.")
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})

@login_required
def list_products(request):
    products = Product.objects.all()
    return render(request, 'catalog/list_products.html', {'products': products})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('list_products')
    return render(request, 'catalog/delete_product.html', {'product': product})   

    