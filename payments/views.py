from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import binascii
import hashlib
from urllib.parse import urlencode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from .service import PaymentService

# Create your views here.


MerchantID = settings.ENCRYPTION_KEY["MERCHANT_ID"]
HASHKEY = settings.ENCRYPTION_KEY["HASH_KEY"]
HASHIV = settings.ENCRYPTION_KEY["HASH_IV"]
Version = settings.ENCRYPTION_KEY["VERSION"]
ReturnUrl = settings.ENCRYPTION_KEY["RETURN_URL"]
NotifyUrl = settings.ENCRYPTION_KEY["NOTIFY_URL"]
PayGateWay = settings.ENCRYPTION_KEY["PAY_GATEWAY"]
RespondType = settings.ENCRYPTION_KEY["RESPOND_TYPE"]


def upgrade(request):
    return render(request, "payments/upgrade.html")


@require_POST
def create_order(request):
    member = request.user
    price = request.POST["price"]
    return PaymentService(member, price).call(request)


@csrf_exempt
def newpay_return(request):
    print(request)
    return render(request, "payments/success.html")
