from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .models import Post
from .forms import PostForm,CommentForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Relation
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


User = get_user_model()


class HomeView(View):
    def get(self,request,*args, **kwargs):
        posts = Post.published.all()
        return render(request, 'home/index.html',context={'posts':posts})


class PostDetailView(View):
    form_class = CommentForm
    
    def setup(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        self.post_instance = get_object_or_404(Post, pk=post_pk)
        return super().setup(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        form = self.form_class()
        comments = self.post_instance.comments.filter(is_reply=False)
        return render(request, 'home/post_detail.html',context={'post':self.post_instance,'comments':comments, 'form':form})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        post = self.post_instance
        if form.is_valid:
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            messages.success(request, 'comment added to the post!')
            return redirect('home:post_detail',pk=post.pk, post_slug=post.slug)
        messages.warning(request, 'an error accrued on creating comment check your inputs please!!')
        return redirect('home:post_detail',pk=post.pk, post_slug=post.slug)
        


class PostEditView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        self.post_instance = get_object_or_404(Post, pk=post_pk)
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.author.id != request.user.id:
            messages.error(request, 'you cant update this post!!')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = PostForm(instance=post)
        return render(request, 'home/post_edit.html', {'form':form,'post':post})
    
    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, 'post successfully edited!')
            return redirect('home:home')
        form = PostForm(instance=post)
        return render(request, 'home/post_edit.html', {'form':form,'post':post})
    

class PostCreateView(LoginRequiredMixin, View):
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


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        post = get_object_or_404(Post, id=post_id)
        if post.author.id != request.user.id:
            messages.error(request, 'you cant delete this post!!')
            return redirect('home:home')
        post.delete()
        messages.success(request, 'post successfully deleted!!')
        return redirect('home:home')
    
    
class FollowingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        to_user = User.objects.get(pk=pk)
        following , created = Relation.objects.get_or_create(to_user=to_user, from_user=request.user)
        if created:
            messages.success(request, f'user {to_user} is added to your following list!!')
        else:
            messages.error(request, f'you already following {to_user} user!!')
        return redirect('accounts:user_panel', pk=pk)
    
    
class UnFollowingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        to_user = User.objects.get(pk=pk)
        following = Relation.objects.filter(to_user=to_user, from_user=request.user)
        if following.exists:
            following.first().delete()
            messages.success(request, f'you successfully unfollowed user {to_user} ')
        else:
            messages.error(request, f'you are not following {to_user} user!!')
        return redirect('accounts:user_panel', pk=pk)
    

class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_pk = kwargs.get('post_pk')
        comment_pk = kwargs.get('comment_pk')
        post = get_object_or_404(Post, pk=post_pk)
        comment = post.comments.get(pk=comment_pk)
        if comment and comment.user == request.user:
            comment.delete()
            messages.success(request, 'message removed!!')
            return redirect('home:post_detail', pk=post.pk, post_slug=post.slug)
        messages.error(request, 'invalid request!!')
        return redirect('home:post_detail',pk=post.pk, post_slug=post.slug)