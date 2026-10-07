import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garba_connect.settings')
django.setup()

from accounts.models import User, UserProfile, City
from matching.models import ConnectionRequest, Match, GarbaPlan
from chat.models import Conversation, Message
from events.models import GarbaEvent

def wipe_all_test_data():
    print("Wiping out all test data...")
    
    # Delete all chats and matches
    Message.objects.all().delete()
    Conversation.objects.all().delete()
    GarbaPlan.objects.all().delete()
    Match.objects.all().delete()
    ConnectionRequest.objects.all().delete()
    
    # Delete all users EXCEPT superusers
    User.objects.filter(is_superuser=False).delete()
    
    # Make sure we have our basic cities to test with
    if not City.objects.exists():
        City.objects.create(name='Indore', state='Madhya Pradesh')
        City.objects.create(name='Ahmedabad', state='Gujarat')
        City.objects.create(name='Mumbai', state='Maharashtra')
        City.objects.create(name='Surat', state='Gujarat')
        City.objects.create(name='Vadodara', state='Gujarat')
        
    print("Clean sweep complete! The platform is now totally fresh and ready for testing from scratch.")

if __name__ == '__main__':
    wipe_all_test_data()
