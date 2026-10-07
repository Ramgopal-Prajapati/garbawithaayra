from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from matching.models import Match
from .models import Conversation, Message

@login_required
def chat_view(request, match_id):
    from django.db.models import Q
    match = get_object_or_404(Match, id=match_id)
    
    # Ensure user is part of the match
    if match.user_one != request.user.profile and match.user_two != request.user.profile:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    conversation, created = Conversation.objects.get_or_create(match=match)
    messages = conversation.messages.all().order_by('created_at')
    
    other_user = match.user_two if match.user_one == request.user.profile else match.user_one
    
    return render(request, 'chat/chat.html', {
        'match': match,
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user
    })

@login_required
def send_message(request, match_id):
    if request.method == 'POST':
        match = get_object_or_404(Match, id=match_id)
        if match.user_one != request.user.profile and match.user_two != request.user.profile:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
            
        conversation = match.conversation
        text = request.POST.get('message', '')
        attachment = request.FILES.get('attachment')
        
        if text or attachment:
            msg = Message.objects.create(
                conversation=conversation,
                sender=request.user.profile,
                message=text,
                attachment=attachment
            )
            return JsonResponse({
                'status': 'success',
                'message': msg.message,
                'file_url': msg.attachment.url if msg.attachment else None
            })
        return JsonResponse({'error': 'Empty message'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def react_message(request, message_id):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            reaction = data.get('reaction')
            msg = get_object_or_404(Message, id=message_id)
            
            # Security check: User must be part of the conversation
            if msg.conversation.match.user_one != request.user.profile and msg.conversation.match.user_two != request.user.profile:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
                
            msg.reaction = reaction
            msg.save()
            return JsonResponse({'status': 'success', 'reaction': reaction})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
