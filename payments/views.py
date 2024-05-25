from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from .service import PaymentService
import binascii
import os
import json
from .models import Payment

# Create your views here.

@login_required
def upgrade(request):
    return render(request, "payments/upgrade.html")


@require_POST
@login_required
def create_order(request):
    member = request.user
    price = request.POST["price"]
    order = PaymentService(member, price).call(request)
    return render(request, 'payments/check.html', order)


@csrf_exempt
def newpay_return(request):
    if request.method == "POST":
        params = request.POST.get("TradeInfo")
        if params:
            try:
                key = os.getenv("HASHKEY").encode("utf-8")
                iv = os.getenv("HASHIV").encode("utf-8")

                # 將十六進位轉換為二進位
                encrypted_data = binascii.unhexlify(params)

                # 用 AES 方式解除雜湊並解密
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()
                decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

                # 移除數據的填充
                plain = strip_padding(decrypted_data)

                response = json.loads(plain)

                # 更新Payment & member
                order = response["Result"]["MerchantOrderNo"]
                price = response["Result"]["Amt"]
                trade_no = response["Result"]["TradeNo"]
                status = response["Status"]
                paid_at = response["Result"]["PayTime"]

                Payment.objects.filter(order=order, price=price).update(
                    trade_no=trade_no, status=status, paid_at=paid_at
                )

                payment = Payment.objects.get(order=order)
                member = payment.member

                if  payment.price >= 200:
                    member.level = "svip"  
                elif payment.price >= 100:
                    member.level = "vvip"  
                elif payment.price >= 50:
                    member.level = "vip"  
                else:
                    member.level = "basic"  

                member.save()

                return render(request, 'payments/success.html')
            except Exception as e:
                return HttpResponse(
                    f"Error: {str(e)}", status=500, content_type="text/plain"
                )
        else:
            return HttpResponse(
                "No TradeInfo provided", status=400, content_type="text/plain"
            )
    else:
        return HttpResponse(
            "Invalid request method", status=405, content_type="text/plain"
        )

# 移除填充字節
def strip_padding(data):
    slast = data[-1]
    return data[:-slast].decode("utf-8")

