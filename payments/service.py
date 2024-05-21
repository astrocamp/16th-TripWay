from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
import binascii
import hashlib
from urllib.parse import urlencode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

MerchantID = settings.ENCRYPTION_KEY["MERCHANT_ID"]
HASHKEY = settings.ENCRYPTION_KEY["HASH_KEY"]
HASHIV = settings.ENCRYPTION_KEY["HASH_IV"]
Version = settings.ENCRYPTION_KEY["VERSION"]
ReturnUrl = settings.ENCRYPTION_KEY["RETURN_URL"]
NotifyUrl = settings.ENCRYPTION_KEY["NOTIFY_URL"]
PayGateWay = settings.ENCRYPTION_KEY["PAY_GATEWAY"]
RespondType = settings.ENCRYPTION_KEY["RESPOND_TYPE"]


class PaymentService:
    def __init__(self, member, price):
        self.member = member
        self.price = price
        self.timestamp = int(timezone.now().timestamp())

    def prepare_data(self):
        data = {
            "MerchantID": MerchantID,
            "RespondType": RespondType,
            "TimeStamp": self.timestamp,
            "Version": "2.0",
            "MerchantOrderNo": self.timestamp,
            "Amt": str(self.price),
            "ItemDesc": "MemberUpgrade",
            "ReturnURL": ReturnUrl,
        }
        return data

    def encrypt_data(self, data_query):
        key = HASHKEY.encode("utf-8")
        iv = HASHIV.encode("utf-8")

        # 對數據進行填充，使其長度為塊大小的倍數
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data_query) + padder.finalize()

        # 創建AES-256-CBC加密對象
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # 使用加密對象加密數據
        # 將加密結果轉換為十六進制表示
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return binascii.hexlify(ciphertext).decode("utf-8")

    def create_hash(self, edata):
        # 構建hashs字符串
        # 計算SHA-256並轉換為大寫
        hashs = f"HashKey={HASHKEY}&{edata}&HashIV={HASHIV}"
        return hashlib.sha256(hashs.encode("utf-8")).hexdigest().upper()

    def call(self, request):
        data = self.prepare_data()
        data_query = urlencode(data).encode("utf-8")
        edata = self.encrypt_data(data_query)
        hash_result = self.create_hash(edata)

        content = {
            "MerchantID": MerchantID,
            "TradeInfo": edata,
            "TradeSha": hash_result,
            "Version": Version,
            "member": self.member,
            "price": self.price,
        }

        return render(request, 'payments/check.html', content)
