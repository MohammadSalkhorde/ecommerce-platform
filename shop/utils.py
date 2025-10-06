#----------------------------------------------------------------------
#----------------------------------------------------------------------
from random import randint

def create_random_code(count):
    count-=1
    return randint(10**count,10**(count+1)-1)
#----------------------------------------------------------------------
#----------------------------------------------------------------------
from kavenegar import *

def send_sms(mobile,message):
    # api = KavenegarAPI('')
    # params = { 'sender' : '2000660110', 'receptor': mobile, 'message' :message }
    # response = api.sms_send(params)
    pass
#----------------------------------------------------------------------
#----------------------------------------------------------------------
from uuid import uuid4
import os

class UploadFile:
    def __init__(self,dir,prefix):
        self.dir = dir
        self.prefix = prefix
    
    def upload_to(self,instance,filename):
        filename, ext =os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'
#----------------------------------------------------------------------
def price_by_delivery_tax(price,discount=0):
    delivery=25000
    if price>500000:
        delivery=0
    tax=(price+delivery)*0.09
    sum=price+delivery+tax
    sum=sum-(sum*discount/100)
    return int(sum),delivery,int(tax)
#----------------------------------------------------------------------