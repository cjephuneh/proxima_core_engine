from django.conf import settings
from python_flutterwave import payment


payment.token = settings.FW_SECRET_KEY
