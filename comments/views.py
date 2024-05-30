from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from spots.models import Spot
from django.contrib import messages
from .models import Comment
from .forms import CommentForm

def index(request):
    if request.method == 'POST':
        if 'comment' in request.POST and 'rating' in request.POST:
            comment_content = request.POST.get('comment')
            rating_value = request.POST.get('rating')
            spot_id = request.POST.get('spot', None)  # 獲取 spot_id，可以為空

            if comment_content and rating_value:
                spot = get_object_or_404(Spot, id=spot_id) if spot_id else None
                Comment.objects.create(content=comment_content, spot=spot, user=request.user, value=int(rating_value))
                request.session['alert'] = {'type': 'success', 'message': "已提交留言！"}
            else:
                request.session['alert'] = {'type': 'error', 'message': "請先完成評分！"}
            return redirect('comments:index')

        if 'edit_comment_id' in request.POST:
            comment_id = request.POST['edit_comment_id']
            comment = get_object_or_404(Comment, id=comment_id)
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                request.session['alert'] = {'type': 'success', 'message': "留言已修改！"}

            return redirect('comments:index')

        if 'delete_comment_id' in request.POST:
            comment_id = request.POST['delete_comment_id']
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
            request.session['alert'] = {'type': 'success', 'message': "留言已刪除！"}
            return redirect('comments:index')

    comments = Comment.objects.all()
    form = CommentForm()
    spots = Spot.objects.all()
    alert = request.session.pop('alert', None)
    return render(request, 'comments/index.html', {'comments': comments, 'form': form, 'spots': spots, 'alert': alert})
    