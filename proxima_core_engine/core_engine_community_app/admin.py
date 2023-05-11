from django.contrib import admin

from core_engine_community_app.models import (
    Comment, Community, Issue, Thread
)





@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'thread', )
    raw_id_fields = ('thread', 'client')
    # autocomplete_fields = ('skills',)

    search_fields = ('comment_id',)
    
    fieldsets = (
        (None, {
            'fields': ('comment_id', 'thread', 'client', 'likes', 'dislikes')
        }),
        ('Metadata', {
            #'classes': ('collapse',),
            'fields': ('metadata',),
        }),
        # ('Advanced options', {
        #     'classes': ('collapse',),
        #     'fields': ('item',),
        # }),
    )


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('community_id', 'tenant_id', 'description')
    raw_id_fields = ('tenant_id',)

    search_fields = ('community_id', )


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('issue_id', 'client_id', 'issue','community_id', 'description', 'solved')
    raw_id_fields = ('client_id',)

    search_fields = ('issue_id', )


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('thread_id', 'issue')
    raw_id_fields = ('issue',)

    search_fields = ('thread_id', )

