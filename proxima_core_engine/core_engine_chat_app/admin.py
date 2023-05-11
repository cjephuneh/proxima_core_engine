from django.contrib import admin

from core_engine_chat_app.models import (
    Chat, ClientChats, Message, TenantChats

)


# class ChatPositionInline(admin.TabularInline):
#     model = chat.Chat
#     verbose_name = 'Course'
#     verbose_name_plural = 'Courses'
#     raw_id_fields = ('course',)
#     extra = 0


# class PathwayItemPositionInline(admin.TabularInline):
#     model = PathwayItemPosition
#     verbose_name = 'Pathway Item'
#     verbose_name_plural = 'Pathway Items'
#     raw_id_fields = ('item',)
#     extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'tenant', 'guest_client', 'chat_owner')
    raw_id_fields = ('tenant', 'chat_owner')
    # autocomplete_fields = ('skills',)

    search_fields = ('chat_id',)
    
    # fieldsets = (
    #     (None, {
    #         'fields': ('chat_id', 'tenant', 'chat_owner')
    #     }),
    #     ('Metadata', {
    #         #'classes': ('collapse',),
    #         'fields': ('metadata',),
    #     }),
    #     ('Advanced options', {
    #         'classes': ('collapse',),
    #         'fields': ('item',),
    #     }),
    # )


@admin.register(ClientChats)
class ClientChatsAdmin(admin.ModelAdmin):
    list_display = ('client_chats_id', 'client_id', 'chat_id')
    raw_id_fields = ('client_id', 'chat_id')

    search_fields = ('client_chats_id', 'client_id')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'chat_id', 'text_content', 'voice_content', 'sent_at', 'message_sender')
    raw_id_fields = ('chat_id',)

    search_fields = ('message_id', )


@admin.register(TenantChats)
class TenantChatsAdmin(admin.ModelAdmin):
    # inlines = (ProgramCoursePositionInline,)
    tenant_chats_id = ('tenant_chats_id', 'tenant_id', 'chat_id')
    raw_id_fields = ('tenant_id',)
    # autocomplete_fields = ('skills',)

    search_fields = ('tenant_chats_id',)
    list_filter = ('tenant_chats_id', 'tenant_id')
    
    fieldsets = (
        (None, {
            'fields': ('tenant_chats_id', 'tenant_id', 'name', 'chat_id')
        }),
        ('Metadata', {
            'fields': ('metadata',),
        }),
        # ('Advanced options', {
        #     #'classes': ('collapse',),
        #     'fields': ('enabled',),
        # }),
    )

