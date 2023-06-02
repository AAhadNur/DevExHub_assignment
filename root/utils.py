# This file contains 3 functions to avoid redundant code in views.py

import json
from . models import *


# cookieCart function retrieves shopping cart info from front-end
"""
    If any customer does not create an account but wants to purchase any product 
    then this function will retrieve shopping cart info ( total number of items in cart, 
    order details, individual itmes)
"""


def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cartItems = order['get_cart_items']

    for i in cart:

        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }

            items.append(item)

        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


"""
    if user is registered then cart info will be saved in database and cartData function will
    retrieve info from database.
    otherwise this function will get data from front-end by cookieCart functions. And return 
    those data when it will be called.
"""


def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


"""
    if anyone is not registered and wants to purchase any product then guestOrder function
    will automatically create a customer profile with the help of shipping info. And the function 
    will save order details and the customer in the database
"""


def guestOrder(request, data):

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)

    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order
