from django.db import models
from accounts.models import UserProfile, City

class ConnectionRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
    ]
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')

class Match(models.Model):
    user_one = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='matches_as_one')
    user_two = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='matches_as_two')
    status = models.CharField(max_length=20, default='MATCHED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_one', 'user_two')

class GarbaPlan(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='plans')
    date = models.DateField()
    time = models.TimeField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    venue = models.CharField(max_length=255)
    meetup_point = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='PROPOSED')
    proposed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
