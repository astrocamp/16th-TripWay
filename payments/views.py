from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings

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
    timestamp = timezone.now().timestamp()
    data = {
        "MerchantID": mid,
        "RespondType": "String",
        "TimeStamp": int(time.time()),
        "Version": "2.0",
        "MerchantOrderNo": f"Vanespl_ec_{int(time.time())}",
        "Amt": f"{request.POST['price']}",
        "ItemDesc": "test",
        "NotifyURL": "https://webhook.site/97c6899f-077b-4025-9948-9ee96a38dfb7",
    }


