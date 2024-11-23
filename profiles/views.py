from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import FriendRequest
from django.contrib.auth import get_user_model
from django.db.models import Q
from news.models import Post
from .models import Profile, FriendRequest
from messages_app.models import Conversation
from news.forms import PostForm
from django.contrib import messages
from users.models import CustomUser
from .forms import ProfileMediaForm
from .models import Media
from .forms import MediaForm


@login_required
def view_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    # Форма для создания поста
    post_form = PostForm()

    if request.method == 'POST' and request.user == profile.user:
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user  # Устанавливаем текущего пользователя автором
            post.save()
            return redirect('view_profile', username=username)

    # Проверяем, отправил ли текущий пользователь запрос
    sent_request = FriendRequest.objects.filter(
        sender=request.user,
        receiver=profile.user,
        status='pending'
    ).exists()

    # Проверяем, получил ли текущий пользователь запрос от этого профиля
    received_request = FriendRequest.objects.filter(
        sender=profile.user,
        receiver=request.user,
        status='pending'
    ).exists()

    # Проверяем, являются ли пользователи друзьями
    is_friend = profile.friends.filter(id=request.user.profile.id).exists()

    # Проверяем, существует ли диалог между пользователями
    conversation = Conversation.objects.filter(
        participants__in=[request.user]
    ).filter(
        participants__in=[profile.user]
    ).first()

    # Получение медиа (фото и видео)
    photos = profile.media.filter(media_type='image')  # Фото
    videos = profile.media.filter(media_type='video')  # Видео

    return render(request, 'profiles/profile_view.html', {
        'profile': profile,
        'post_form': post_form,
        'sent_request': sent_request,
        'received_request': received_request,
        'is_friend': is_friend,
        'conversation_id': conversation.id if conversation else None,
        'photos': photos,  # Передаём фото в шаблон
        'videos': videos,  # Передаём видео в шаблон
    })




@login_required
def edit_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile', username=username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile_edit.html', {'form': form})


User = get_user_model()

@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    # Проверяем, что запрос ещё не отправлен
    if not FriendRequest.objects.filter(sender=request.user, receiver=receiver, status='pending').exists():
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
    return redirect('view_profile', username=receiver.username)

@login_required
def respond_to_friend_request(request, request_id, response):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    if response == 'accept':
        friend_request.status = 'accepted'
        friend_request.save()
        # Логика добавления друзей (многие-ко-многим)
        request.user.profile.friends.add(friend_request.sender.profile)
    elif response == 'decline':
        friend_request.status = 'declined'
        friend_request.save()
    return redirect('view_profile', username=request.user.username)

@login_required
def friends_list(request):
    search_query = request.GET.get('search', '')
    search_results = []

    if search_query:
        search_results = CustomUser.objects.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        ).exclude(id=request.user.id)

    friends = request.user.profile.friends.all()
    incoming_requests = FriendRequest.objects.filter(receiver=request.user)
    outgoing_requests = FriendRequest.objects.filter(sender=request.user)

    # Получение всех пользователей для глобального поиска
    all_users = CustomUser.objects.exclude(id=request.user.id)

    return render(request, 'profiles/friends_list.html', {
        'search_results': search_results,
        'friends': friends,  # Список друзей
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'all_users': all_users,
    })




@login_required
def media_gallery(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(author=profile.user).exclude(image=None, video=None)

    return render(request, 'profiles/media_gallery.html', {
        'profile': profile,
        'posts': posts
    })

# messages_app/views.py

@login_required
def start_conversation(request, user_id):
    user_to_message = get_object_or_404(User, id=user_id)

    # Проверяем, существует ли уже диалог
    conversation = Conversation.objects.filter(
        participants__in=[request.user]
    ).filter(
        participants__in=[user_to_message]
    ).first()

    if not conversation:
        # Создаём новый диалог
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, user_to_message)

    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def remove_friend(request, user_id):
    friend_profile = get_object_or_404(Profile, user__id=user_id)
    user_profile = request.user.profile

    if friend_profile in user_profile.friends.all():
        user_profile.friends.remove(friend_profile)
        friend_profile.friends.remove(user_profile)
        messages.success(request, f'Вы удалили {friend_profile.user.get_full_name() or friend_profile.user.username} из друзей.')
    else:
        messages.error(request, 'Этот пользователь не является вашим другом.')

    return redirect('friends_list')

@login_required
def upload_media(request):
    if request.method == 'POST':
        form = ProfileMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.profile = request.user.profile
            media.save()
            return redirect('view_profile', username=request.user.username)
    else:
        form = ProfileMediaForm()
    
    return render(request, 'profiles/upload_media.html', {'form': form})

@login_required
def add_photo(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            Media.objects.create(
                profile=request.user.profile,
                file=file,
                media_type='image'
            )
            messages.success(request, 'Фото успешно добавлено!')
        else:
            messages.error(request, 'Вы не выбрали файл.')
    return redirect('view_profile', username=request.user.username)


@login_required
def add_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        Media.objects.create(
            user=request.user,
            file=video,
            media_type='video'
        )
    return redirect('view_profile', username=request.user.username)

@login_required
def add_media(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    if request.method == 'POST' and request.user == profile.user:
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.profile = profile
            media.save()
            return redirect('view_profile', username=username)
    else:
        form = MediaForm()
    return render(request, 'profiles/add_media.html', {'form': form, 'profile': profile})