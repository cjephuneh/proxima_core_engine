# Generated by Django 4.1.7 on 2023-04-05 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core_engine_tenant_management_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chat_id', models.AutoField(help_text='The chat ID UUID for an instance of a chat.', primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TenantChats',
            fields=[
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tenant_chats_id', models.AutoField(help_text='The tenant chats ID UUID for all chats.', primary_key=True, serialize=False)),
                ('chat_id', models.ForeignKey(help_text='Display name of the chat', on_delete=django.db.models.deletion.CASCADE, to='core_engine_chat_app.chat')),
                ('tenant_id', models.ForeignKey(help_text='Display name of the tenant', on_delete=django.db.models.deletion.CASCADE, to='core_engine_tenant_management_app.tenant')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message_id', models.AutoField(help_text='The message ID UUID for an instance of a chat.', primary_key=True, serialize=False)),
                ('text_content', models.CharField(blank=True, help_text='Message text content', max_length=255, null=True)),
                ('voice_content', models.FileField(blank=True, help_text='The voice note sent', null=True, upload_to='media/voice_content')),
                ('sent_at', models.DateTimeField(auto_now_add=True, help_text='Time that the message has been sent')),
                ('message_sender', models.CharField(choices=[('client', 'client'), ('tenant', 'tenant'), ('tenant_iva', 'tenant_iva')], help_text='Either the message is sent by the agent or by the tenant', max_length=50)),
                ('chat_id', models.ForeignKey(help_text='The chat ID UUID for an instance of a chat.', on_delete=django.db.models.deletion.CASCADE, to='core_engine_chat_app.chat')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientChats',
            fields=[
                ('metadata', models.JSONField(blank=True, help_text='Metadata', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_chats_id', models.AutoField(help_text='The chat ID UUID for an instance of a chat.', primary_key=True, serialize=False)),
                ('chat_id', models.ForeignKey(help_text='Display name of the chat', on_delete=django.db.models.deletion.CASCADE, to='core_engine_chat_app.chat')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at', '-metadata'],
                'abstract': False,
            },
        ),
    ]
