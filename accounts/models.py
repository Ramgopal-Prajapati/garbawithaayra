from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator

class UserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError('Either email or phone must be set')
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, password=password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email or self.phone or str(self.id)

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}, {self.state}"

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending Verification'),
        ('SINGLE', 'Single - Looking for Garba Partner'),
        ('COMMITTED', 'Partner Chosen'),
        ('BREAK', 'Taking a Break'),
    ]
    VERIFICATION_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=30, unique=True, null=True) # Added for unique public handles
    display_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_CHOICES, default='PENDING')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    garba_experience = models.CharField(max_length=50, blank=True)
    preferred_style = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name

class ProfilePhoto(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='gallery_photos')
    image = models.ImageField(upload_to='gallery_photos/')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class IdentityVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='identity_verification')
    verification_method = models.CharField(max_length=50)
    verification_status = models.CharField(max_length=20, default='PENDING')
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='verifications_done')

