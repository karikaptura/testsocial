from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Conversation


User = get_user_model()

@login_required
def conversation_list(request):
    conversations = request.user.conversations.all()
    conversation_data = []

    total_unread = 0  # Счётчик для всех непрочитанных сообщений

    for conversation in conversations:
        participant = conversation.participants.exclude(id=request.user.id).first()
        unread_count = conversation.messages.filter(
            ~Q(sender=request.user),  # Сообщения не от текущего пользователя
            is_read=False
        ).count()
        total_unread += unread_count  # Добавляем непрочитанные сообщения в общий счётчик

        last_message = conversation.messages.last()  # Получаем последнее сообщение
        conversation_data.append({
            'conversation': conversation,
            'participant': participant,
            'unread_count': unread_count,
            'last_message': last_message.content if last_message else "Нет сообщений",
        })

    search_query = request.GET.get('search', '')
    search_results = []

    if search_query:
        # Поиск по пользователям
        user_results = User.objects.filter(
            Q(username__icontains=search_query) | 
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query),
        ).exclude(id=request.user.id)

        # Поиск по содержимому сообщений
        message_results = Message.objects.filter(
            Q(content__icontains=search_query) & 
            Q(conversation__participants=request.user)
        ).distinct()

        search_results = {
            'users': user_results,
            'messages': message_results
        }

    return render(request, 'messages_app/conversation_list.html', {
        'conversations': conversation_data,
        'search_results': search_results,
        'search_query': search_query,
        'total_unread': total_unread,  # Передаём общий счётчик в шаблон
    })



@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.order_by('created_at')
    participant = conversation.participants.exclude(id=request.user.id).first()
    
    return render(request, 'messages_app/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'participant': participant,
    })




@login_required
def send_message(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id)
        content = request.POST.get('content')
        if content.strip():
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Проверяем, AJAX ли запрос
                return JsonResponse({
                    'id': message.id,
                    'sender': message.sender.username,
                    'content': message.content,
                    'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
        return redirect('conversation_detail', conversation_id=conversation_id)

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Проверяем, существует ли уже диалог
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect('conversation_detail', conversation_id=conversation.id)


@login_required
def fetch_new_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Получаем сообщения, отправленные другим пользователем, и не прочитанные
    new_messages = conversation.messages.filter(
        ~Q(sender=request.user),
        is_read=False
    )
    
    # Отмечаем их как прочитанные
    new_messages.update(is_read=True)
    
    # Формируем список сообщений для ответа
    messages_data = [
        {
            'id': message.id,
            'sender': message.sender.username,
            'content': message.content,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in new_messages
    ]
    
    return JsonResponse({'messages': messages_data})


