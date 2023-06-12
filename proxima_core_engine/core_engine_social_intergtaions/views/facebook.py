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

# FACEBOOK_TOKEN = os.environ.get("FACEBOOK_MESSENGER_TOKEN")
FACEBOOK_TOKEN = 'EAAEpg4FEZB5cBAAZBdwId6qY64qi59tSizZA4ZAqbCi9NrszTFB2tOl7Ngw4em7KzSOYbM4hzaZCrbu2LAZBAawSDK8uGd92b9RbwB1StNof72HCF0kZBe64wFuZCe7jclGEadfZB6C95c6cCQMoQbKAlHqLmk4W4yCj0pFOhQz1c76ZAgzfjXp4tE'
FACEBOOK_API_URL = "https://graph.facebook.com/v14.0/me/messages?access_token={}".format(FACEBOOK_TOKEN)

"""
Instantiating redis
"""
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)

class FaceBookIntergration(APIView):
    # Disable CSRF protection for this view
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        VERIFY_TOKEN = "meatyhamhock"

        if 'hub.mode' in request.GET and 'hub.verify_token' in request.GET:
            mode = request.GET.get('hub.mode')
            token = request.GET.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                challenge = request.GET.get('hub.challenge')
                return JsonResponse({'hub.challenge': challenge}, status=200)
            else:
                return Response('ERROR', status=403)

        return Response('SOMETHING', status=200)

    def post(self, request):
        headers = {'content-type': 'application/json'}

        body = request.data
        entries = body['entry']
        for entry in entries:
            webhookEvent = entry['messaging'][0]
            senderPsid = webhookEvent['sender']['id']
            user_query = webhookEvent['message']['text']

            k = str(uuid.uuid4())
            d = {"id": k, "user_query": user_query, "Contact": senderPsid, "chatmeans": "Facebook"}

            db.rpush(settings.TEXT_QUEUE, json.dumps(d))

            while True:
                output = db.get(k)

                if output is not None:
                    chat_response = json.loads(output)
                    db.delete(k)
                    break

                time.sleep(settings.CLIENT_SLEEP)

            text_message = {
                "recipient": {
                    "id": senderPsid
                },
                "message": {
                    "text": chat_response[0]['chatbot_response']
                },
                'messaging_type': 'RESPONSE'
            }

            response = requests.post(settings.FACEBOOK_API_URL, json=text_message, headers=headers)
            response_json = response.json()

            return Response({
                "data": response_json,
                "status": "success",
            }, status=200)
