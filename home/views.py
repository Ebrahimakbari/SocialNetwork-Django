from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
from .models import Post
# Create your views here.


class HomeView(View):
    def get(self,request,*args, **kwargs):
        posts = Post.published.all()
        return render(request, 'home/index.html',context={'posts':posts})


class PostDetailView(View):
    def get(self,request,*args, **kwargs):
        post_pk = kwargs.get('pk')
        post = Post.published.get(pk=post_pk)
        return render(request, 'home/post_detail.html',context={'post':post})