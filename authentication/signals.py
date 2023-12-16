from authentication.models import Tokens, Otp
from django.contrib.auth.tokens import default_token_generator
from django.db.models.signals import Signal
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


user_created = Signal()
otp_created = Signal()


@receiver(post_save, sender=get_user_model())
def after_user_created(sender, instance, created, **kwargs):
    """will be called when new user is created"""
    if created:
        """we are creating a new token for verification"""
        token = default_token_generator.make_token(instance)
        Tokens.objects.create(token=token, user=instance)
        user_created.send(sender=sender, token=token)


@receiver(post_save, sender=Otp)
def after_otp_created(sender, instance, created, **kwargs):
    """will be called when new otp is created"""
    if created:
        """we will send the otp"""
        otp_created.send(sender=sender, instance=instance)
