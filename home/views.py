from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
# Create your views here.


class HomeView(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'home/index.html',context={})