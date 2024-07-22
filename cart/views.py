from django.shortcuts import render, get_object_or_404
from .cart import Cart
from catalog.models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
@csrf_exempt
def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty'))
        
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product=product, quantity=product_qty)
        
        return JsonResponse({'qty': cart.__len__()})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def cart_delete(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        cart = Cart(request)
        cart.delete(product=product_id)
        
        return JsonResponse({'qty': cart.__len__()})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def cart_update(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty'))
        
        cart = Cart(request)
        cart.update(product=product_id, quantity=product_qty)
        
        return JsonResponse({'qty': cart.__len__()})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prod()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals})