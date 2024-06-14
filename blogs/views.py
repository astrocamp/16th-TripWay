from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from .forms import BlogForm, BlogCommentForm
from .models import Blog, BlogComment
from django.core.files.storage import default_storage
from django.db import IntegrityError
import base64
from django.core.files.base import ContentFile

def index(request):
    sort_option = request.GET.get('sort', 'created_at_desc')
    if sort_option == 'views_desc':
        blogs = Blog.objects.all().order_by('-views')
    elif sort_option == 'comment_count_desc':
        blogs = Blog.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')
    else:
        blogs = Blog.objects.all().order_by('-created_at')

    return render(request, 'blogs/index.html', {'blogs': blogs, 'sort_option': sort_option})

def article(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = BlogComment.objects.filter(blog=blog)
    blog.views += 1
    blog.save()

    if request.method == 'POST':
        if 'content' in request.POST:
            form = BlogCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()
                messages.success(request, "評論已成功提交！")
            else:
                messages.error(request, "評論提交失敗，請檢查內容。")
        elif 'edit_comment_id' in request.POST:
            comment_id = request.POST.get("edit_comment_id")
            comment_content = request.POST.get("edit_comment_content")
            if comment_id and comment_content:
                try:
                    comment = get_object_or_404(BlogComment, id=comment_id, user=request.user)
                    comment.content = comment_content
                    comment.save()
                    messages.success(request, "評論已修改！")
                except IntegrityError:
                    messages.error(request, "評論修改失敗，請檢查內容。")
        elif 'delete_comment_id' in request.POST:
            comment_id = request.POST.get("delete_comment_id")
            if comment_id:
                try:
                    comment = get_object_or_404(BlogComment, id=comment_id, user=request.user)
                    comment.delete()
                    messages.success(request, "評論已刪除！")
                except IntegrityError:
                    messages.error(request, "評論刪除失敗。")
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
        return redirect("blogs:index")

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "文章已成功更新！")
            return redirect("blogs:index")
        else:
            messages.error(request, "表單有誤，請檢查輸入內容。")
    else:
        form = BlogForm(instance=blog)
    return render(request, "blogs/edit.html", {"form": form, "blog": blog})

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if blog.user != request.user:
        messages.error(request, "您沒有權限刪除此文章。")
        return redirect("blogs:index")
    
    if request.method == "POST":
        blog.delete()
        messages.success(request, "文章已刪除！")
    return redirect("blogs:index")

@csrf_exempt
@login_required
def image_upload(request):
    if request.method == 'POST':
        cropped_image_data = request.POST.get('croppedImage')
        if cropped_image_data:
            format, imgstr = cropped_image_data.split(';base64,')
            ext = format.split('/')[-1]
            cropped_image = ContentFile(base64.b64decode(imgstr), name='cropped_image.' + ext)
            filename = default_storage.save(cropped_image.name, cropped_image)
            url = default_storage.url(filename)
            return JsonResponse({'url': url})
    return JsonResponse({'error': 'Invalid request'}, status=400)