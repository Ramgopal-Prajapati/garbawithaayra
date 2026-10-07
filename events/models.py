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
