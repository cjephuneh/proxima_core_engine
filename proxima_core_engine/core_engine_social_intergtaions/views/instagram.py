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


"""
Instantiating redis
"""
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)


"""
INSTAGRAM AUTOMATION ENDPOINT
"""
# INSTAGRAM_TOKEN = os.environ.get("INSTAGRAM_TOKEN")
INSTAGRAM_TOKEN = 'EAAEpg4FEZB5cBALeFGHH1ZAZCuX9Sff61FvhwAx7JMjlSVUrMxVR25L1qdYjoOsYZBxRZBFrk8GVmP8WKBGMZB4ZAU5i1jjcKZBLD4ZA5Oa8ZCbdNDDx8vtKVsuww6paHpliZCEg4CKok1NdkQwgSaeZCOu1n5fRWJgddtTPsvqbskojyyOzuZBelRXcZB'
INSTAGRAM_API_URL = "https://graph.facebook.com/v14.0/me/messages?access_token={}".format(INSTAGRAM_TOKEN)
#Function to access the Sender API
                       
class InstagramIntergration(APIView):
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
        headers = {
            "Content-Type": "application/json",
        }

        VERIFY_TOKEN = "meatyhamhock"

        if 'hub.mode' in request.GET and 'hub.verify_token' in request.GET:
            mode = request.GET.get('hub.mode')
            token = request.GET.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                challenge = request.GET.get('hub.challenge')
                return JsonResponse({'hub.challenge': challenge}, status=200)
            else:
                return Response('ERROR', status=403)

        data = request.data
        body = json.loads(data.decode('utf-8'))

        if 'object' in body:
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                IGSID = webhookEvent['sender']['id']
                user_query = webhookEvent['message']['text']
                print(user_query)
                print('Sender IGSID: {}'.format(IGSID))

        k = str(uuid.uuid4())
        d = {"id": k, "user_query": user_query, "Contact": IGSID, "chatmeans": "Instagram"}
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
                "id": IGSID
            },
            "message": {
                "text": chat_response[0]['chatbot_response']
            },
        }

        response = requests.post(settings.INSTAGRAM_API_URL, json=text_message, headers=headers)
        response_json = response.json()

        return Response({
            "data": response_json,
            "status": "success",
        }, status=200)
