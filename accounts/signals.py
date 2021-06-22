
from django.db.models.signals import post_save, post_delete
from .models import CustomUser
from django.dispatch import receiver # Import the receiver
from .models import Profile


@receiver(post_save, sender=CustomUser) 
def create_profile(sender, instance, created, **kwargs):
    """ when a user is created - create an attched Profile"""
    if created:
        Profile.objects.create(user=instance)


#@receiver(post_save, sender=CustomUser)
#def save_profile(sender, instance, **kwargs):
#    instance.profile.save()


@receiver(post_delete, sender=Profile)
def post_delete_profile_clean_image(sender, instance, **kwargs):
    cond = instance.image.name != instance.image.field.default

    if cond and instance.image:
        instance.image.delete(save=False)
