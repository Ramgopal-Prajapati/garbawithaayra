from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile, City
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        display_name = request.POST.get('display_name')
        age = request.POST.get('age')
        bio = request.POST.get('bio')
        password = request.POST.get('password')
        profile_photo = request.FILES.get('profile_photo')

        # Validation
        if not username:
            return render(request, 'accounts/register.html', {
                'error_message': 'Username is required.',
                'form_data': request.POST
            })
            
        import re
        if not re.match(r'^[\w]+$', username):
            return render(request, 'accounts/register.html', {
                'error_message': 'Username can only contain letters, numbers, and underscores.',
                'form_data': request.POST
            })

        if UserProfile.objects.filter(username__iexact=username).exists():
            return render(request, 'accounts/register.html', {
                'error_message': 'This username is already taken. Please choose another.',
                'form_data': request.POST
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {
                'error_message': 'This email is already registered. Please login or use a different email.',
                'form_data': request.POST
            })
            
        if User.objects.filter(phone=phone).exists():
            return render(request, 'accounts/register.html', {
                'error_message': 'This phone number is already registered.',
                'form_data': request.POST
            })

        gallery_photos = request.FILES.getlist('gallery_photos')
        if not age or not bio or not profile_photo:
            return render(request, 'accounts/register.html', {
                'error_message': 'Please fill out all required fields, including Age, Bio, and Profile Picture.',
                'form_data': request.POST
            })
            
        if len(gallery_photos) < 3:
            return render(request, 'accounts/register.html', {
                'error_message': 'You must upload at least 3 gallery photos to verify your profile.',
                'form_data': request.POST
            })

        # Create user manually to guarantee password is set correctly
        user = User.objects.create_user(email=email, phone=phone, password=password)
        
        # Create Profile
        profile = UserProfile.objects.create(
            user=user,
            username=username,
            display_name=display_name,
            age=age,
            bio=bio,
            profile_photo=profile_photo,
            verification_status='PENDING'
        )
        
        from .models import ProfilePhoto
        for f in gallery_photos[:5]: # Max 5 photos initially
            ProfilePhoto.objects.create(profile=profile, image=f, is_approved=True)
        
        # Authenticate and login using the raw password to ensure session is valid
        auth_user = authenticate(request, email=email, password=password)
        if auth_user:
            login(request, auth_user)
        
        return redirect('dashboard')
        
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def edit_profile(request):
    from .models import ProfilePhoto
    profile = request.user.profile
    if request.method == 'POST':
        profile.display_name = request.POST.get('display_name', profile.display_name)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.age = request.POST.get('age', profile.age)
        profile.garba_experience = request.POST.get('garba_experience', profile.garba_experience)
        
        # Handle single profile photo update
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
            
        profile.save()
        
        # Handle multiple gallery photo uploads
        if 'gallery_photos' in request.FILES:
            for f in request.FILES.getlist('gallery_photos'):
                # Limit to 5 photos total to prevent spam
                if profile.gallery_photos.count() < 5:
                    ProfilePhoto.objects.create(
                        profile=profile,
                        image=f,
                        is_approved=True # Auto-approve for demo
                    )
                    
        return redirect('dashboard')
        
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

@login_required
def delete_gallery_photo(request, photo_id):
    from .models import ProfilePhoto
    from django.shortcuts import get_object_or_404
    photo = get_object_or_404(ProfilePhoto, id=photo_id, profile=request.user.profile)
    photo.delete()
    return redirect('edit_profile')
