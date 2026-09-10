"""
Custom data loader that handles signal conflicts.
"""
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.db import connection, transaction
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from commerce.models import Profile

# Try to disconnect signals
try:
    from commerce.signals import create_user_profile, save_user_profile
    post_save.disconnect(create_user_profile, sender=User)
    post_save.disconnect(save_user_profile, sender=User)
    print("✓ Signals disconnected")
except Exception as e:
    print(f"⚠ Could not disconnect signals: {e}")

# Load the datadump
with open('/app/datadump.json', 'r') as f:
    data = json.load(f)

print(f"📦 Loaded {len(data)} objects from datadump.json")

# Separate user and profile objects
users_data = [obj for obj in data if obj['model'] == 'auth.user']
profiles_data = [obj for obj in data if obj['model'] == 'commerce.profile']
other_data = [obj for obj in data if obj['model'] not in ('auth.user', 'commerce.profile')]

print(f"  Users: {len(users_data)}")
print(f"  Profiles: {len(profiles_data)}")
print(f"  Others: {len(other_data)}")

# Clear everything first
with transaction.atomic():
    Profile.objects.all().delete()
    User.objects.all().delete()
    print("✓ Cleared existing users and profiles")

# Write remaining data to temp file
temp_data = users_data + other_data
with open('/app/temp_dump.json', 'w') as f:
    json.dump(temp_data, f, indent=2)

print(f"✓ Wrote {len(temp_data)} non-profile objects to temp_dump.json")

# Load users and other data first (Django will auto-create profiles)
from django.core.management import call_command
call_command('loaddata', '/app/temp_dump.json')
print("✓ Loaded users and other data")

# Now update profiles with the data from datadump
from django.apps import apps
profile_model = apps.get_model('commerce', 'Profile')

# Get the natural key fields for Profile
print("📦 Updating profiles with original data...")
updated_count = 0
for profile_data in profiles_data:
    fields = profile_data['fields']
    # Find the user
    user_id = fields.get('user')
    if isinstance(user_id, list):
        # natural key format
        try:
            user = User.objects.get(username=user_id[0])
            user_id = user.id
        except User.DoesNotExist:
            continue
    
    try:
        profile = Profile.objects.get(user_id=user_id)
        # Update fields
        for key, value in fields.items():
            if key != 'user':
                setattr(profile, key, value)
        profile.save()
        updated_count += 1
    except Profile.DoesNotExist:
        pass

print(f"✓ Updated {updated_count} profiles")
print("🎉 Data load complete!")
