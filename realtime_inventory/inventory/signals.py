from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import OrderSerializer

@receiver(post_save, sender=Order)
def broadcast_order(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        data = {
            "type": "send_update",
            "data": {
                "event": "order_created",
                "order": OrderSerializer(instance).data
            }
        }
        async_to_sync(channel_layer.group_send)("live_updates", data)
