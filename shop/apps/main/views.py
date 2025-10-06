from django.shortcuts import render
from django.conf import settings
from .models import *
from django.views import View

def media_admin(request):
    return {'media':settings.MEDIA_URL,}


def index(request):
    return render(request,'main_app/index.html')

class SliderView(View):
    def get(self,request):
        sliders=Slider.objects.filter(is_active=True)
        return render(request,'main_app/sliders.html',{'sliders':sliders})
    
def handler404(request, exception=None):
    return render(request,'main_app/404.html')