from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from accounts.models import UserProfile
from .models import ConnectionRequest, Match
from chat.models import Conversation

@login_required
@require_POST
def send_request(request, receiver_id):
    try:
        sender_profile = request.user.profile
        receiver_profile = UserProfile.objects.get(id=receiver_id)
        
        if sender_profile == receiver_profile:
            return JsonResponse({'error': 'Cannot send request to yourself'}, status=400)
            
        # Check if they are already matched
        if Match.objects.filter(user_one=sender_profile, user_two=receiver_profile).exists() or Match.objects.filter(user_one=receiver_profile, user_two=sender_profile).exists():
            return JsonResponse({'error': 'You are already matched with this user!'}, status=400)
            
        # Check if a pending request already exists
        if ConnectionRequest.objects.filter(sender=sender_profile, receiver=receiver_profile, status='PENDING').exists():
            return JsonResponse({'error': 'Request already sent and is pending.'}, status=400)
            
        # Check if they already sent you a pending request
        if ConnectionRequest.objects.filter(sender=receiver_profile, receiver=sender_profile, status='PENDING').exists():
            return JsonResponse({'error': 'They already sent you a request! Check your dashboard.'}, status=400)
            
        # Update existing old request (e.g., from unmatch/decline) or create a new one
        ConnectionRequest.objects.update_or_create(
            sender=sender_profile, 
            receiver=receiver_profile,
            defaults={'status': 'PENDING'}
        )

                # Send Email Notification asynchronously
        if receiver_profile.user.email:
            import threading
            from django.core.mail import send_mail
            from django.conf import settings
            
            def send_async_email():
                try:
                    subject = "New Garba Partner Request! 💃🕺"
                    message = f"Hi {receiver_profile.display_name},\n\n{sender_profile.display_name} (@{sender_profile.username}) has sent you a connection request for Garba!\n\nLog in to your Garba with Aayra dashboard to accept or decline the request.\n\nKeep Dancing,\nGarba with Aayra Team"
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [receiver_profile.user.email], fail_silently=True)
                except Exception as e:
                    pass
                    
            threading.Thread(target=send_async_email).start()
        return JsonResponse({'message': 'Interest sent successfully!'})
        
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def accept_request(request, request_id):
    from django.db.models import Q
    try:
        conn_req = ConnectionRequest.objects.get(id=request_id, receiver=request.user.profile, status='PENDING')
        
        # Check if either user is already matched
        if Match.objects.filter(Q(user_one=conn_req.sender) | Q(user_two=conn_req.sender)).exists():
            return JsonResponse({'error': 'The sender already found a partner.'}, status=400)
        if Match.objects.filter(Q(user_one=conn_req.receiver) | Q(user_two=conn_req.receiver)).exists():
            return JsonResponse({'error': 'You already have a partner. Unmatch first.'}, status=400)
            
        conn_req.status = 'ACCEPTED'
        conn_req.save()
        
        # Update user statuses
        conn_req.sender.status = 'COMMITTED'
        conn_req.receiver.status = 'COMMITTED'
        conn_req.sender.save()
        conn_req.receiver.save()
        
        # Create Match
        match = Match.objects.create(user_one=conn_req.sender, user_two=conn_req.receiver)
        
        # Create Conversation
        Conversation.objects.create(match=match)
        
        return JsonResponse({'message': 'Match created successfully!'})
    except ConnectionRequest.DoesNotExist:
        return JsonResponse({'error': 'Request not found or already processed'}, status=404)

@login_required
@require_POST
def decline_request(request, request_id):
    try:
        conn_req = ConnectionRequest.objects.get(id=request_id, receiver=request.user.profile, status='PENDING')
        conn_req.status = 'DECLINED'
        conn_req.save()
        return JsonResponse({'message': 'Request declined'})
    except ConnectionRequest.DoesNotExist:
        return JsonResponse({'error': 'Request not found'}, status=404)

@login_required
@require_POST
def unmatch(request, match_id):
    try:
        from django.db.models import Q
        match = Match.objects.get(id=match_id)
        if match.user_one != request.user.profile and match.user_two != request.user.profile:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
            
        # Revert statuses to SINGLE
        match.user_one.status = 'SINGLE'
        match.user_two.status = 'SINGLE'
        match.user_one.save()
        match.user_two.save()
        
        # Delete match (cascades to Conversation and Messages)
        match.delete()
        
        return JsonResponse({'message': 'Unmatched successfully.'})
    except Match.DoesNotExist:
        return JsonResponse({'error': 'Match not found'}, status=404)






@login_required
@require_POST
def withdraw_request(request, request_id):
    try:
        conn_req = ConnectionRequest.objects.get(id=request_id, sender=request.user.profile, status='PENDING')
        conn_req.delete()
        return JsonResponse({'message': 'Request withdrawn successfully'})
    except ConnectionRequest.DoesNotExist:
        return JsonResponse({'error': 'Request not found'}, status=404)
