import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garba_connect.settings')
django.setup()

from accounts.models import User, UserProfile, City
from events.models import GarbaEvent

def seed():
    print("Clearing old data...")
    User.objects.exclude(is_superuser=True).delete()
    City.objects.all().delete()
    GarbaEvent.objects.all().delete()

    print("Creating cities...")
    indore = City.objects.create(name='Indore', state='Madhya Pradesh')
    ahmedabad = City.objects.create(name='Ahmedabad', state='Gujarat')
    mumbai = City.objects.create(name='Mumbai', state='Maharashtra')

    print("Creating events...")
    GarbaEvent.objects.create(
        name="Indore Grand Navratri", date=date(2026, 10, 15), city=indore,
        venue="Vijay Nagar Ground", address="Vijay Nagar", 
        start_time="19:00", end_time="23:30", description="Biggest garba in Indore!"
    )

    print("Creating users...")
    users_data = [
        {"email": "rahul@test.com", "phone": "9876543210", "name": "Rahul", "gender": "M", "city": indore, "exp": "Intermediate", "bio": "Love traditional garba!"},
        {"email": "priya@test.com", "phone": "9876543211", "name": "Priya", "gender": "F", "city": indore, "exp": "Advanced", "bio": "Looking for a partner who knows dodhiya."},
        {"email": "amit@test.com", "phone": "9876543212", "name": "Amit", "gender": "M", "city": ahmedabad, "exp": "Beginner", "bio": "First time doing garba, need a friendly partner."},
        {"email": "neha@test.com", "phone": "9876543213", "name": "Neha", "gender": "F", "city": mumbai, "exp": "Intermediate", "bio": "Mumbai garba nights! Let's go."},
        {"email": "karan@test.com", "phone": "9876543214", "name": "Karan", "gender": "M", "city": indore, "exp": "Advanced", "bio": "Can teach you step by step."},
    ]

    for data in users_data:
        u = User.objects.create_user(email=data['email'], phone=data['phone'], password='password123')
        u.is_verified = True
        u.save()
        UserProfile.objects.create(
            user=u,
            display_name=data['name'],
            gender=data['gender'],
            city=data['city'],
            bio=data['bio'],
            garba_experience=data['exp'],
            status='SINGLE',
            verification_status='APPROVED'
        )
    print("Successfully seeded 5 users, cities, and events!")

if __name__ == '__main__':
    seed()
