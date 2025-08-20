from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Product, Customer, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "stock")
    search_fields = ("name", "sku")
    list_filter = ("stock",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email")


# Inline for Order Items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    def save_new_instance(self, form, commit=True):
        """Ensure stock validation is respected in admin."""
        try:
            instance = form.save(commit=False)
            instance.full_clean()
            if commit:
                instance.save()
            return instance
        except ValidationError as e:
            form.add_error(None, e)
            raise


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "customer", "created_at", "total")
    readonly_fields = ("total",)  # total cannot be manually edited

    def save_model(self, request, obj, form, change):
        """Save order and recalc total."""
        super().save_model(request, obj, form, change)
        obj.recalc_total()  # update total after saving order

    def save_formset(self, request, form, formset, change):
        """Recalculate total when saving inline order items."""
        instances = formset.save(commit=False)
        for instance in instances:
            instance.full_clean()  # validate stock
            instance.save()
        formset.save_m2m()

        # Recalculate total for the order
        if form.instance.pk:
            form.instance.recalc_total()
