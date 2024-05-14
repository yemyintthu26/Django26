from django.shortcuts import render, redirect
from myshop.models import Product, Cart, Order
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def to_home(request):
    return redirect('/product/list')

@login_required(login_url='login')
def PorductList(request):
    if request.GET.get('c'):
        category = request.GET.get('c')
        products = Product.objects.filter(category_id=category)
    else:
        products = Product.objects.all()
    return render(request, 'productList.html',{'products':products})

@login_required(login_url='login')
def PorductDetail(request, post_id):
    product = Product.objects.get(id=post_id)
    return render(request, 'productDetail.html',{'product':product})

def CartCreate(request, pdt_id):
    cart = Cart.objects.create(
        product = Product.objects.get(id=pdt_id),
        qty = request.GET.get('qty'),
        user_id = request.user.id,
        created_at = datetime.now()
    )
    cart.save()
    messages.success(request, f"Added {cart.product.name} successfully.")
    return redirect(f'/product/list/')

def CartList(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    for item in cart:
        item.total = item.product.price * item.qty
    return render(request, 'cartList.html',{'cart':cart})

def CartDelete(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    messages.success(request, f"Deleted {cart.product.name} successfully.")
    return redirect(f'/product/cartList/')

def buyNow(request,post_id):
    product = Product.objects.get(id = post_id)
    product.qty = request.GET.get('qty')
    product.total = product.price * int(product.qty)
    if request.method == "GET":
        return render(request, 'orderCreate.html',{'product':product})
    if request.method == "POST":
        Myproduct = []
        Myproduct.append({
            'id':product.id, 
            'image':product.image.url,
            'name':product.name, 
            'price':product.price, 
            'qty':product.qty, 
            'total':product.total
            }) 
        order = Order.objects.create(
            product = Myproduct,
            user_id = request.user.id,
            total_price = product.total,
            total_qty = product.qty,
            name = request.POST.get('name'),
            phone = request.POST.get('phone'),
            address = request.POST.get('address'),
            created_at = datetime.now()
        )
        messages.success(request, "Order successfully.")
        return redirect(f'/product/list/')
    
def cartOrderCreate(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    product = []
    total = 0
    total_qty = 0
    for c in cart:
        product.append({
            'id':c.product.id, 
            'image':c.product.image.url,
            'name':c.product.name, 
            'price':c.product.price, 
            'qty':c.qty, 
            'total':c.product.price * c.qty
            })
        total += c.product.price * c.qty
        total_qty += c.qty
    order = Order.objects.create(
        product = product,
        user_id = request.user.id,
        total_price = total,
        total_qty = total_qty,
        name = request.POST.get('name'),
        phone = request.POST.get('phone'),
        address = request.POST.get('address'),
        created_at = datetime.now()
    )
    cart.delete()
    messages.success(request, "Order successfully.")
    return redirect(f'/product/list/')

def orderList(request):
    orders = Order.objects.filter(user_id = request.user.id)
    for o in orders:
        o.id = o.id.hex[:8]
    return render(request, 'orderList.html',{'orders':orders})

def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html') 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password) 
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully.")
            return redirect('/product/list')
        else:
            messages.error(request, "Username or Password is incorrect!.")
            return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logout successfully.")
    return redirect('/login/')
