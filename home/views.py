from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.urls import reverse
from django.views import View
from .models import Post
from .forms import PostForm
from django.contrib import messages
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


class PostEditView(View):
    def get(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        post = Post.objects.get(pk=post_pk)
        form = PostForm(instance=post)
        return render(request, 'home/post_edit.html', {'form':form,'post':post})
    
    def post(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        post = Post.objects.get(pk=post_pk)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, 'post successfully edited!')
            return redirect('home:home')
        form = PostForm(instance=post)
        return render(request, 'home/post_edit.html', {'form':form,'post':post})
    

class PostCreateView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'home/post_create.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, 'post successfully created!')
            return redirect('home:home')
        messages.error(request, 'post not created!')
        return render(request, 'home/post_create.html', {'form':form})


class PostDeleteView(View):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        post = Post.objects.get(id=post_id)
        post.delete()
        messages.success(request, 'post successfully deleted!!')
        return redirect('home:home')