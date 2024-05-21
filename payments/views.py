from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .service import PaymentService

# Create your views here.

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
