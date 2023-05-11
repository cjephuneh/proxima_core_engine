import uuid
from datetime import datetime
from django.db import models
from core_engine_utils_app.models import MetaDataBase
from core_engine_tenant_users_app.models import Client
# Settimg up the chat body template


"""
When a tenant is created a community is created for that tenant - signals
"""
class Community(MetaDataBase):
    community_id = models.AutoField(primary_key=True,
                                    help_text="The tenant community ID UUID.")
    community_name = models.CharField(max_length=255, null=True, blank=True,
                                      help_text="Display name of the community.")
    tenant_id = models.ForeignKey("core_engine_tenant_management_app.Tenant", on_delete=models.CASCADE,
                                   help_text="Display name of the tenant.")    
    description = models.TextField(max_length=255, 
                                    help_text="Description of the community.", null=True, blank=True)
    members = models.ManyToManyField(Client,
                                      help_text="Members of the community.", blank=True)


    def __str__(self):
        return str(self.community_id)

    def add_client_to_community(self, client):
        '''A helper function to add a user to a group and create an event object.'''
        event, created = self.event_set.get_or_create(type="Join", client=client)
        if created:
            event.timestamp = datetime.now()
            event.save()
        self.members.add(client)
        self.save()
        return event

    def remove_client_from_community(self, client):
        '''An helper function to remove users from group members when they \
        leave the group and create an event for the timestamp the Client left the group.'''
        try:
            event = self.event_set.get(type="Left", client=client)
        except Event.DoesNotExist:
            event = self.event_set.create(type="Left", client=client)
            event.timestamp = datetime.now()
            event.save()
        self.members.remove(client)
        self.save()
        return event

class Event(models.Model):
    '''
    A model that holds all events related to a community like when a Client joins the group or leaves.
    '''
    CHOICES = [
        ("Join", "join"),
        ("Left", "left")
        ]
    type = models.CharField(choices=CHOICES, max_length=10)
    description= models.CharField(help_text="A description of the event that occurred",\
    max_length=50, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(Community ,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.description = f"{self.client} {self.type} the {self.community.tenant_id} group"
        super().save(*args, kwargs)

    def __str__(self) -> str:
        return f"{self.description}"
    
class Rating(MetaDataBase):
    rating_id = models.AutoField(primary_key=True,
                                            help_text="The tenant community rating ID.")
    community_id = models.ForeignKey("core_engine_community_app.Community", on_delete=models.CASCADE,
                                help_text="Display name of the Community", null=True)
    client_id = models.ForeignKey("core_engine_tenant_users_app.Client", on_delete=models.CASCADE,
                                help_text="Display name of the client")
    rating = models.IntegerField(default=0) 



    def __str__(self):
        return str(self.rating_id)