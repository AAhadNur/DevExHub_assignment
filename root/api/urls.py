from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.getProducts),
    path('store/<str:pk>/', views.getSpecificProduct),
    path('order/', views.OrderCreateAPIView.as_view()),
    path('place/', views.PlaceOrderAPIView.as_view()),
]
