from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import redis
import uuid
import json
import time
import requests

API_URL = "https://graph.facebook.com/v15.0/110409438554070/messages" 
# API_TOKEN = os.environ.get("API_TOKEN")
API_TOKEN = 'EAAEpg4FEZB5cBAHpmn5CTILpZCtYzGaZA7GrKWbnzCEV12Q6LaeuJwrbvUvvOo9FW0Y2WkY0rATe9DprsTjIZBPMZAq2xaTLA6TxqOdrPjmqS33t9X0PA2UTSkVKh0UGEm6BojPrYtvHtKHfJKhQNzIdeFHUVl57yCTT80sSnyU49Cep6IqFuZC5Fb84Qh8AiZBGEtTZB1VkagZDZD'
 
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)


class WhatsAppIntergration(APIView):
    # Disable CSRF protection for this view
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        headers = {
            "Authorization": f"Bearer {settings.API_TOKEN}",
            "Content-Type": "application/json",
        }

        data = request.data

        try:
            k = str(uuid.uuid4())
            d = {"id": k, "user_query": data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'],
                 "Contact": data['entry'][0]['changes'][0]['value']['messages'][0]['from'], "chatmeans": "WhatsApp"}

            try:
                d = {"id": k, "user_query": data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'],
                     "Contact": data['entry'][0]['changes'][0]['value']['messages'][0]['from'], "chatmeans": "WhatsApp"}
            except:
                print("No new message")
            db.rpush(settings.TEXT_QUEUE, json.dumps(d))

            while True:
                output = db.get(k)
                db.delete(k)

                if output is not None:
                    chat_response = json.loads(output)

                    text_message = {
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": data['entry'][0]['changes'][0]['value']['messages'][0]['from'],
                        "type": "text",
                        "text": {
                            "preview_url": False,
                            "body": chat_response[0]['chatbot_response']
                        }
                    }

                    response = requests.post(url=settings.API_URL, headers=headers, json=text_message)
                    print(response.json())
                    response_json = response.json()

                    break

                time.sleep(settings.CLIENT_SLEEP)

            return Response({
                "data": response_json,
                "status": "success",
            }, status=200)

        except:
            return Response({
                "data": "response_json",
                "status": "success",
            }, status=200)
