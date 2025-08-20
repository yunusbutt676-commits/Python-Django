from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Customer, Order, OrderItem
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, F

@api_view(['GET'])
def top_products(request):
    items = (OrderItem.objects
             .values('product__id', 'product__name')
             .annotate(qty=Sum('quantity'))
             .order_by('-qty')[:10])
    data = [{'id': it['product__id'], 'name': it['product__name'], 'qty': it['qty']} for it in items]
    return Response(data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by("-created_at")
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer

# Frontend dashboard page
class DashboardView(TemplateView):
    template_name = "inventory/dashboard.html"
