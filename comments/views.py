from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Comment, Rating
from .forms import CommentForm

def index(request):
    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_content = request.POST.get('comment', None)
            rating_value = request.POST.get('rating', None)

            if comment_content and rating_value:
                comment = Comment.objects.create(content=comment_content)
                Rating.objects.create(value=int(rating_value), comment=comment)
                messages.success(request, '留言已保存')
                print(f"留言已保存: {comment_content}，評分: {rating_value}")
            return redirect('comments:index')

        elif 'edit_comment_id' in request.POST:
            comment_id = request.POST['edit_comment_id']
            comment = get_object_or_404(Comment, id=comment_id)
            comment.content = request.POST.get('edit_comment_content', comment.content)
            comment.save()
            messages.success(request, '留言已更新')
            return redirect('comments:index')

        elif 'delete_comment_id' in request.POST:
            comment_id = request.POST['delete_comment_id']
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
            messages.success(request, '留言已刪除')
            return redirect('comments:index')

    comments = Comment.objects.all()
    form = CommentForm()
    return render(request, 'comments/index.html', {'comments': comments, 'form': form})
