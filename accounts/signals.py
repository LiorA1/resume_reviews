
from django.db.models.signals import post_save, post_delete
from .models import CustomUser, Profile
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser, dispatch_uid='post_save_create_profile')
def create_profile(sender, instance, created, **kwargs):
    """Called when a CustomUser is created, and creates an attched Profile"""
    if created:
        Profile.objects.create(user=instance)


# @receiver(post_save, sender=CustomUser)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()


@receiver(post_delete, sender=Profile, dispatch_uid='post_delete_clean_image')
def post_delete_profile_clean_image(sender, instance, **kwargs):
    """Called when a profile is deleted, for erase the image from AWS S3 storage."""
    cond = instance.image.name != instance.image.field.default

    if cond and instance.image:
        instance.image.delete(save=False)
