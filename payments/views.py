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
    timestamp = int(timezone.now().timestamp())

    data = {
        "MerchantID": MerchantID,
        "RespondType": RespondType,
        "TimeStamp": timestamp,
        "Version": "2.0",
        "MerchantOrderNo": timestamp,
        "Amt": f"{request.POST['price']}",
        "ItemDesc": "MemberUpgrade",
        "ReturnURL": ReturnUrl,
    }

    data_query = urlencode(data).encode("utf-8")

    key = HASHKEY.encode("utf-8")
    iv = HASHIV.encode("utf-8")

    # 對數據進行填充，使其長度為塊大小的倍數
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data_query) + padder.finalize()

    # 創建AES-256-CBC加密對象
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # 使用加密對象加密數據
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # 將加密結果轉換為十六進制表示
    edata = binascii.hexlify(ciphertext).decode("utf-8")

    # 構建hashs字符串
    hashs = f"HashKey={HASHKEY}&{edata}&HashIV={HASHIV}"

    # 計算SHA-256並轉換為大寫
    hash_result = hashlib.sha256(hashs.encode("utf-8")).hexdigest().upper()

    return render(request, 'payments/check.html', {
        'MerchantID': MerchantID,
        'TradeInfo': edata,
        'TradeSha': hash_result,
        'Version': Version,
        'member': member,
        'price': price,
    })


@csrf_exempt
def newpay_return(request):
    print(request)
    return render(request, "payments/success.html")
