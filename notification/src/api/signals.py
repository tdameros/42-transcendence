import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from api.models import Notification


@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'{instance.owner_id}',
            {
                'type': 'send_notification',
                'message': json.dumps({
                    'title': instance.title,
                    'type': instance.type
                })
            }
        )