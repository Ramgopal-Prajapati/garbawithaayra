from django.shortcuts import render
from accounts.models import UserProfile
from events.models import GarbaEvent
from django.contrib.auth.decorators import login_required

def home(request):
    profiles = UserProfile.objects.filter(verification_status='APPROVED').order_by('-created_at')[:6]
    return render(request, 'core/index.html', {'profiles': profiles})

def discover(request):
    # Get approved and single profiles
    profiles = UserProfile.objects.filter(
        verification_status='APPROVED',
        status='SINGLE'
    ).exclude(user=request.user if request.user.is_authenticated else None)
    
    # Apply search filters
    username_q = request.GET.get('username')
    location_q = request.GET.get('location')
    
    from django.db.models import Q
    if username_q:
        username_q = username_q.lstrip('@')
        profiles = profiles.filter(username__icontains=username_q)
        
    if location_q:
        profiles = profiles.filter(
            age=location_q # reusing the old location_q param for age just in case, but really we removed location search.
        )
    
    # We only exclude the logged in user themselves. The status='SINGLE' already filters out matched users!
    return render(request, 'core/discover.html', {'profiles': profiles})

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
        
        # Get matching data
        from matching.models import ConnectionRequest, Match
        from django.db.models import Q
        
        incoming_requests = ConnectionRequest.objects.filter(receiver=profile, status='PENDING')
        outgoing_requests = ConnectionRequest.objects.filter(sender=profile, status='PENDING')
        matches = Match.objects.filter(Q(user_one=profile) | Q(user_two=profile))
        
    except UserProfile.DoesNotExist:
        profile = None
        incoming_requests = []
        outgoing_requests = []
        matches = []
        
    return render(request, 'core/dashboard.html', {
        'profile': profile,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'matches': matches
    })

def events_list(request):
    events = GarbaEvent.objects.all()
    return render(request, 'core/events.html', {'events': events})

@login_required
def view_profile(request, profile_id):
    from django.shortcuts import get_object_or_404
    profile = get_object_or_404(UserProfile, id=profile_id)
    return render(request, 'core/profile_detail.html', {'target_profile': profile})

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def is_staff_check(user):
    return user.is_active and user.is_staff

@user_passes_test(is_staff_check, login_url='/login/')
def mainadmin_dashboard(request):
    users = UserProfile.objects.all().order_by('-created_at')
    pending_count = UserProfile.objects.filter(verification_status='PENDING').count()
    approved_count = UserProfile.objects.filter(verification_status='APPROVED').count()
    
    return render(request, 'core/mainadmin.html', {
        'users': users,
        'pending_count': pending_count,
        'approved_count': approved_count
    })

@user_passes_test(is_staff_check, login_url='/login/')
def mainadmin_approve(request, profile_id):
    from django.shortcuts import get_object_or_404
    profile = get_object_or_404(UserProfile, id=profile_id)
    profile.verification_status = 'APPROVED'
    profile.status = 'SINGLE'
    profile.save()
    return redirect('mainadmin_dashboard')

@user_passes_test(is_staff_check, login_url='/login/')
def mainadmin_reject(request, profile_id):
    from django.shortcuts import get_object_or_404
    profile = get_object_or_404(UserProfile, id=profile_id)
    profile.verification_status = 'REJECTED'
    profile.save()
    return redirect('mainadmin_dashboard')

@user_passes_test(is_staff_check, login_url='/login/')
def mainadmin_delete(request, user_id):
    from accounts.models import User
    from django.shortcuts import get_object_or_404
    user_obj = get_object_or_404(User, id=user_id)
    if not user_obj.is_superuser:
        user_obj.delete()
    return redirect('mainadmin_dashboard')
