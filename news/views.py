from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.http import JsonResponse
from .models import Like, Post
from .forms import CommentForm

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Добавлено request.FILES
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('news_feed')
    else:
        form = PostForm()
    return render(request, 'news/create_post.html', {'form': form})

@login_required
def news_feed(request):
    # Получаем все посты, отсортированные по времени создания (от новых к старым)
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'news/news_feed.html', {'posts': posts})


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()  # Удаляем лайк, если уже существует

    return JsonResponse({'likes_count': post.likes.count()})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('news_feed')  # Обновляем страницу

    return redirect('news_feed')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Убедимся, что пост принадлежит текущему пользователю
    if post.author == request.user:
        post.delete()
        return redirect('view_profile', username=request.user.username)  # Замените на нужный маршрут
    else:
        return redirect('view_profile', username=request.user.username)

