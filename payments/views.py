from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .service import PaymentService

# Create your views here.

@login_required
def upgrade(request):
    return render(request, "payments/upgrade.html")


@require_POST
@login_required
def create_order(request):
    member = request.user
    price = request.POST["price"]
    return PaymentService(member, price).call(request)


@csrf_exempt
@login_required
def newpay_return(request):
    print(request)
    return render(request, "payments/success.html")
