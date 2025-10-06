from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import requests
import json
from apps.orders.models import Order,OrderState
from django.core.exceptions import ObjectDoesNotExist
from .models import Payment
from apps.accounts.models import Customer
from apps.warehouses.models import Warehouse,WarehouseType
#----------------------------------------------------------------------------
#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8080/payments/verify/'
#----------------------------------------------------------------------------
class ZarinpalPaymentView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        description="پرداخت از طریق درگاه زرین پال"
        try:
            order=Order.objects.get(id=order_id)
            payment=Payment.objects.create(
                order=order,
                customer=Customer.objects.get(user=request.user),
                amount=order.get_order_total_price(),
                description=description,
            )
            payment.save()
            
            request.session['payment_session']={
                'order_id':order.id,
                'payment_id':payment.id,
            }
            user=request.user
            data = {
                    "MerchantID": settings.MERCHANT,
                    "Amount": order.get_order_total_price(),
                    "Description": description,
                    "Phone": user.phone_number,
                    "CallbackURL": CallbackURL,
                }
            
            data = json.dumps(data)
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            try:
                response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

                if response.status_code == 200:
                    response = response.json()
                    if response['Status'] == 100:
                        return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                    else:
                        return {'status': False, 'code': str(response['Status'])}
                return response
            
            except requests.exceptions.Timeout:
                return {'status': False, 'code': 'timeout'}
            except requests.exceptions.ConnectionError:
                return {'status': False, 'code': 'connection error'}
            
        except ObjectDoesNotExist:
            return redirect('orders:checkout_order',order_id)
#----------------------------------------------------------------------------
class ZarinpalPaymentVerifayView(LoginRequiredMixin,View):
    def get(self,request):
        order_id=request.session['payment_session']['order_id']
        payment_id=request.session['payment_session']['payment_id']
        order=Order.objects.get(id=order_id)
        payment=Payment.objects.get(id=payment_id)
        
        authority=request.GET.get('Authority')
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_order_total_price(),
        "Authority": authority,
    }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                
                order.is_finaly=True
                order.order_state=OrderState.objects.get(id=1)
                order.save()
                
                for item in order.order_details1.all():
                    Warehouse.objects.create(
                        warehouse_type=WarehouseType.objects.get(id=2),
                        user_registered=request.user,
                        product=item.product,
                        qty=item.qty,
                        price=item.price
                    )
                    
                payment.is_finally=True
                payment.status_code=response['Status']
                payment.ref_id=str(response['RefID'])
                payment.save()
                
                return redirect('payments:show_verifay_message',f'پرداخت با موفقیت انجام شد. کد رهگیری شما : {response['RefID']}')
                # return {'status': True, 'RefID': response['RefID']}
            else:
                payment.status_code=response['Status']
                payment.save()
                return redirect('payments:show_verifay_message',f"خطا در فرآیند پرداخت. کد خطا : {response['Status']}")
                # return {'status': False, 'code': str(response['Status'])}
        return response
#----------------------------------------------------------------------------
def show_verifay_message(request,message):
    return render(request,'payments/veify_message.html',message)
#----------------------------------------------------------------------------