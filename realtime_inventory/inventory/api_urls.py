from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProductViewSet, CustomerViewSet, OrderViewSet, top_products

# First create the router
router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('customers', CustomerViewSet)
router.register('orders', OrderViewSet)

# Now extend urlpatterns
urlpatterns = router.urls + [
    path('top-products/', top_products, name='top-products'),
]
