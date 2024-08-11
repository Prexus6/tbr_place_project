from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Book

@receiver(pre_save, sender=Book)
def validate_book_author(sender, instance, **kwargs):
    if instance.book_author is None:
        raise ValueError("Kniha musí mať priradeného autora.")
