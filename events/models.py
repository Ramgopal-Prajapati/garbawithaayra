from django.db import models
from accounts.models import City

class GarbaEvent(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='events')
    venue = models.CharField(max_length=255)
    address = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    poster = models.ImageField(upload_to='event_posters/', null=True, blank=True)
    registration_link = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.city.name}"


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import threading

@receiver(post_save, sender=GarbaEvent)
def notify_users_new_event(sender, instance, created, **kwargs):
    if created:
        def send_mass_emails():
            try:
                from accounts.models import UserProfile
                from django.core.mail import send_mass_mail
                
                users = UserProfile.objects.filter(verification_status='APPROVED').exclude(user__email__isnull=True).exclude(user__email__exact='')
                messages = []
                for profile in users:
                    subject = f"New Garba Event in {instance.city.name}! 🎪"
                    body = f"Hi {profile.display_name},\n\nA new Garba event '{instance.name}' has been added in {instance.city.name}!\n\nDate: {instance.date}\nTime: {instance.start_time}\nVenue: {instance.venue}\n\nCheck out the Events page on Garba with Aayra for more details.\n\nKeep dancing,\nGarba with Aayra"
                    messages.append((subject, body, settings.DEFAULT_FROM_EMAIL, [profile.user.email]))
                
                if messages:
                    send_mass_mail(messages, fail_silently=True)
            except Exception as e:
                pass
                
        threading.Thread(target=send_mass_emails).start()
