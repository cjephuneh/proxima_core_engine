from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator

from .models import Payment
from .services import build_payment_uri


class CheckoutView(LoginRequiredMixin, View):
    """
    Redirects to Flutterwave Payment Checkout
    """
    def get(self, request, **kwargs):
        uri = build_payment_uri(request=request)
        return HttpResponseRedirect(uri)


@method_decorator(csrf_exempt, name='dispatch')
class CallbackView(View):

    def get(self, request, **kwargs):
        tx_ref, tx_id = self.request.GET.get('tx_ref'), self.request.GET.get('transaction_id')
        p = Payment.objects.get(merchant_ref=tx_ref)
        p.transaction_id = tx_id
        p.save()
        return HttpResponse('We have received your payment. We will verify it and get back to you shortly!')
    
    def post(self, request, **kwargs):
        print(request.body.decode('utf-8'))
        return HttpResponse('ok')


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    
    def get(self, request, **kwargs):
        print(request.GET)
        print(request.body)
        return HttpResponse('ok')
    
    def post(self, request, **kwargs):
        print(request.POST)
        print(self.request.body.decode('utf-8'))
        return HttpResponse('ok')
