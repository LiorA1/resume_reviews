
# Objectives:
# 1. Add a signal which inalidate the cache['users_resumes'], when a new resume is added.
# 2. Add a signal which inalidate the cache['users_resumes'], when a resume is deleted.

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Resume

@receiver(post_delete, sender=Resume)
def resume_post_delete_handler(sender, **kwargs):
    cache.clear()
    #print("resume_post_delete_handler 1")
    #print(dir(cache))
    #print(cache.__dict__)
    #print(cache.__repr__)
    #cache.clear(perfix='resume_list')
    #cache.clear()
    #print("resume_post_delete_handler 2")


@receiver(post_save, sender=Resume)
def resume_post_save_handler(sender, **kwargs):
    cache.clear()
    #print("resume_post_save_handler")


#! Notice:
#TODO: Try to solve it.
# Options:
# 1. Create multiple caches
# 2. find a way to find and delete specific enteries in the cache.