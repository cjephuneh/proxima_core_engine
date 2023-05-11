from django.db.models.signals import post_save
from django.dispatch import receiver


from core_engine_community_app.models import Thread, Issue

@receiver(post_save, sender=Issue)
def create_thread_from_issue_raised(sender, instance, created, *args, **kwargs):
    #We are doing this only once when user is created
    if instance and created:
        Thread.objects.create(issue=instance.issue_id)

