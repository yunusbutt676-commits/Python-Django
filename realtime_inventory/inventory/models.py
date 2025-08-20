from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.sku})"


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders")
    created_at = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def recalc_total(self):
        total = sum(i.subtotal for i in self.items.all())
        self.total = total
        self.save()
        return total

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price_at_purchase

    def clean(self):
        # Validate stock before saving
        if not self.pk and self.product.stock < self.quantity:
            raise ValidationError({
                'quantity': f'Not enough stock for {self.product.name}. Available: {self.product.stock}'
            })

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.full_clean()  # triggers clean() and validation
        super().save(*args, **kwargs)

        # Reduce stock only for new items
        if is_new:
            self.product.stock -= self.quantity
            self.product.save()
