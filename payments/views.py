from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .service import PaymentService
import os
import json
import binascii
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.http import HttpResponse

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
        print(request)
        print("-----------------")
        print(params)
        if params:
            try:
                key = os.getenv("HASHKEY").encode("utf-8")
                iv = os.getenv("HASHIV").encode("utf-8")

                # 將十六進位轉換為二進位
                encrypted_data = binascii.unhexlify(params)
                print("-----------------")
                print(encrypted_data)

                # 用 AES 方式解除雜湊
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()

                # 開始解密
                decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
                print("-----------------")
                print(decrypted_data)

                # 移除數據的填充
                plain = strip_padding(decrypted_data)
                print("-----------------")
                print(plain)

                # 解析 JSON 資料
                response = json.loads(plain)
                print("-----------------")
                print(response)

                # 直接返回解密後的原始數據
                return HttpResponse(plain, content_type="text/plain")
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

    #             return JsonResponse(response)
    #         except Exception as e:
    #             return JsonResponse({"error": str(e)}, status=500)
    #     else:
    #         return JsonResponse({"error": "No TradeInfo provided"}, status=400)
    # else:
    #     return JsonResponse({"error": "Invalid request method"}, status=405)

# 移除填充字節
def strip_padding(data):
    slast = data[-1]
    pcheck = data[-slast:]
    if pcheck == bytes([slast]) * slast:
        return data[:-slast].decode("utf-8")
    else:
        return data.decode("utf-8")
