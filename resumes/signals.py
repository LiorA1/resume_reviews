
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Resume

@receiver(post_delete, sender=Resume)
def resume_post_delete_handler(sender, **kwargs):
    """signal which invalidate the cache['users_resumes'], when a resume is deleted."""
    cache.clear()
    #print("resume_post_delete_handler 1")


@receiver(post_save, sender=Resume)
def resume_post_save_handler(sender, **kwargs):
    """signal which invalidate the cache['users_resumes'], when a new resume is added."""
    cache.clear()
    #print("resume_post_save_handler")


@receiver(post_delete, sender=Resume)
def resume_post_delete_handler(sender, instance, **kwargs):
    if instance.resume_file:
        instance.resume_file.delete(save=False)



#! Notice:
#TODO: Try to solve it.
# Options:
# 1. Create multiple caches
# 2. find a way to find and delete specific enteries in the cache.