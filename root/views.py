from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
import json
import datetime

from .models import *
from .utils import cartData, guestOrder

# login view


def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'root/login.html', context)


# logout view
def logoutUser(request):
    logout(request)
    return redirect('store')


# user registration view
def registerUser(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            customer, created = Customer.objects.get_or_create(user=user)
            customer.save()
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'An error occured during registration.')

    context = {'form': form}
    return render(request, 'root/registration.html', context)


# profile view of any specific customer
def userProfile(request, pk):
    customer = Customer.objects.get(id=pk)
    reviews = customer.review_set.all()
    orders = customer.order_set.all()
    address = customer.shippingaddress_set.all()
    context = {'customer': customer, 'reviews': reviews,
               'orders': orders, 'address': address}
    return render(request, 'root/profile.html', context)


# view of all prodcuts with pagination
def store(request):

    data = cartData(request)

    cartItems = data['cartItems']

    p = Paginator(Product.objects.all(), 6)
    page = request.GET.get('page')
    products = p.get_page(page)

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'root/store.html', context)


# view of any specific product
def individualProduct(request, pk):

    data = cartData(request)

    cartItems = data['cartItems']
    product = Product.objects.get(id=pk)
    reviews = product.review_set.all()

    if request.method == "POST":
        review = Review.objects.create(
            customer=request.user.customer,
            product=product,
            body=request.POST.get('body')
        )
        return redirect('product', pk=product.id)

    context = {'product': product, 'cartItems': cartItems, 'reviews': reviews}
    return render(request, 'root/product.html', context)


# if any customer wants to delete his review then this view will handle that
@login_required(login_url='login')
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)

    if request.user.customer != review.customer:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        review.delete()
        return redirect('store')
    return render(request, 'root/delete.html', {'obj': review})


# view of shopping cart
def cart(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'root/cart.html', context)


# view of checkout page
def checkout(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'root/checkout.html', context)


# view to handle product quantity in an order and stock status
def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if product.stock_status >= 1:
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
    if action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


# view for processing an order and save in database
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    orderitems = order.orderitem_set.all()
    for item in orderitems:
        item.product.stock_status -= item.quantity
        item.product.save()

    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )

    return JsonResponse('Payment complete!', safe=False)
