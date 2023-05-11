from django.urls import path
from . import views


app_name = 'core_engine_payments_app'
urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('callback/', views.CallbackView.as_view(), name='callback'),
    path('webhook/', views.WebhookView.as_view(), name='webhook'),
]
