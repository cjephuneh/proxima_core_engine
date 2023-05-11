# import os

# from django.core.asgi import get_asgi_application
# from django.urls import path # new

# from channels.routing import ProtocolTypeRouter, URLRouter # changed

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proxima_core_engine.settings')

# from core_engine_chat_app.consumers import (ChatConsumer, StreamAudioConsumer,
#                           StreamAudioSaveConsumer  )

# from core_engine_community_app.consumers import (
#     CommunityConsumer, GroupConsumer
# )
# # application = ProtocolTypeRouter({
# #     'http': get_asgi_application(),
# #     'websocket': TokenAuthMiddlewareStack( # changed
# #         URLRouter([
# #             path('core/', TaxiConsumer.as_asgi()),
# #             path('chat/', ChatConsumer.as_asgi()),
# #         ])
# #     ),
# # })

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     # new
#     'websocket': URLRouter([
#         path('chat/', ChatConsumer.as_asgi()),
#         path('community/', CommunityConsumer.as_asgi()),
#         path('group/', GroupConsumer.as_asgi()),
#         path('ws/stream_normal_audio/', StreamAudioConsumer.as_asgi()),
#         path('ws/stream_audio/', StreamAudioSaveConsumer.as_asgi()),

#     ]),
# })

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proxima_core_engine.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
})