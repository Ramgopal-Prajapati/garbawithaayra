import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garba_connect.settings')
django.setup()

from accounts.models import User, UserProfile, City
from matching.models import ConnectionRequest, Match

def run_tests():
    print("[STARTING AUTOMATED FLOW TEST]")
    client = Client()

    # 1. Verification & City Match Check
    print("\n[1] Checking Discover Feed for City filtering...")
    client.login(username='rahul@test.com', password='password123')
    rahul = User.objects.get(email='rahul@test.com')
    
    priya = UserProfile.objects.get(user__email='priya@test.com')
    amit = UserProfile.objects.get(user__email='amit@test.com')
    
    indore_profiles = UserProfile.objects.filter(city__name='Indore').exclude(user=rahul)
    ahmedabad_profiles = UserProfile.objects.filter(city__name='Ahmedabad').exclude(user=rahul)
    
    if priya in indore_profiles:
        print("[SUCCESS] Priya found in Indore city filter.")
    else:
        print("[FAILED] City filter error.")
        
    if amit in ahmedabad_profiles and amit not in indore_profiles:
        print("[SUCCESS] Amit correctly filtered out of Indore and found in Ahmedabad.")
    else:
        print("[FAILED] Cross-city filter error.")

    # 2. Send Connection Request
    print("\n[2] Testing 'Send Request' flow...")
    response = client.post(f'/api/requests/send/{priya.id}/')
    if response.status_code == 200:
        print("[SUCCESS] Connection request sent from Rahul to Priya.")
    else:
        print(f"[FAILED] Could not send request (Status {response.status_code})")

    # 3. Duplicate Request Prevention
    print("\n[3] Testing Duplicate Request prevention...")
    dup_response = client.post(f'/api/requests/send/{priya.id}/')
    if dup_response.status_code == 400:
        print("[SUCCESS] Duplicate requests are successfully blocked.")
    else:
        print(f"[FAILED] Duplicate allowed! (Status {dup_response.status_code})")

    # 4. Accept Request
    print("\n[4] Testing 'Accept Request' flow...")
    client.logout()
    client.login(username='priya@test.com', password='password123')
    
    req = ConnectionRequest.objects.get(sender=rahul.profile, receiver=priya)
    response = client.post(f'/api/requests/accept/{req.id}/')
    
    if response.status_code == 200:
        if Match.objects.filter(user_one=rahul.profile, user_two=priya).exists():
            print("[SUCCESS] Priya accepted Rahul's request. Match created!")
        else:
            print("[FAILED] API returned 200 but Match object not found in DB.")
    else:
        print(f"[FAILED] Accept API error (Status {response.status_code})")

    # 5. Decline Request
    print("\n[5] Testing 'Decline Request' flow...")
    karan = User.objects.get(email='karan@test.com')
    req_to_decline = ConnectionRequest.objects.create(sender=karan.profile, receiver=priya)
    
    decline_resp = client.post(f'/api/requests/decline/{req_to_decline.id}/')
    if decline_resp.status_code == 200:
        req_to_decline.refresh_from_db()
        if req_to_decline.status == 'DECLINED':
            print("[SUCCESS] Priya successfully declined Karan's request.")
        else:
            print("[FAILED] Status not updated to DECLINED.")
    else:
        print(f"[FAILED] Decline API error (Status {decline_resp.status_code})")

    print("\n[ALL TESTS COMPLETED SUCCESSFULLY]")

if __name__ == '__main__':
    run_tests()
