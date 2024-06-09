from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BlogForm, BlogCommentForm
from .models import Blog, BlogComment

@login_required
def index(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs/index.html', {'blogs': blogs, 'user': request.user})

@login_required
def article(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = BlogComment.objects.filter(blog=blog)
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            messages.success(request, "評論已成功提交！")
            return redirect('blogs:article', blog_id=blog_id)
    else:
        form = BlogCommentForm()
    return render(request, 'blogs/article.html', {'blog': blog, 'comments': comments, 'form': form})

@login_required
def new(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, "文章已成功建立！")
            return redirect('blogs:index')
        else:
            messages.error(request, "表單有誤，請檢查輸入內容。")
    else:
        form = BlogForm()
    return render(request, 'blogs/new.html', {'form': form})

@login_required
def edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if blog.user != request.user:
        messages.error(request, "您沒有權限編輯此文章。")
        return redirect('blogs:index')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "文章已成功更新！")
            return redirect('blogs:article', blog_id=blog_id)
        else:
            messages.error(request, "表單有誤，請檢查輸入內容。")
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogs/edit.html', {'form': form, 'blog': blog})

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if blog.user != request.user:
        messages.error(request, "您沒有權限刪除此文章。")
    else:
        blog.delete()
        messages.success(request, "文章已刪除！")
    return redirect('blogs:index')
