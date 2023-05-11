import uuid
from django.db import models
from core_engine_utils_app.models import MetaDataBase


class Thread(MetaDataBase):
    """
    When an issue is created - a thread for it is ctreated and all comments are attached to the tread
    """
    thread_id = models.AutoField(primary_key=True,
                                    help_text="The thread ID UUID for an instance of a thread.")
    issue = models.OneToOneField("core_engine_community_app.Issue", on_delete=models.CASCADE,
                            help_text="Display name of the issue that this thread belongs to")


    def __str__(self):
        return str(self.thread_id)
