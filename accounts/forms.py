from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile, City

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    display_name = forms.CharField(max_length=50, required=True, label="Full Name")
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('email', 'phone', 'display_name', 'city', 'address', 'bio', 'profile_photo')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                display_name=self.cleaned_data['display_name'],
                city=self.cleaned_data['city'],
                address=self.cleaned_data['address'],
                bio=self.cleaned_data['bio'],
                profile_photo=self.cleaned_data.get('profile_photo'),
                verification_status='PENDING' # Admin needs to approve
            )
        return user
