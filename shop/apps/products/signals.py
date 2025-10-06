from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import Product
from django.conf import settings
import os

@receiver(post_delete, sender=Product)
def delete_product_image(sender,**kwargs):
    path=settings.MEDIA_ROOT+str(kwargs['instance'].image_name)
    if os.path.isfile(path):
        os.remove(path)
        
        