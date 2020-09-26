from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# def create_new_user_from_oauth_login(name, uid, provider):
#     new_user = User.objects.create_user()



@receiver(signal=user_signed_up, sender=User)
def new_user_from_facebook_login(request, user, **kwargs):
    new_user_profile = UserProfile(user=user, name=user.first_name)
    new_user_profile.save()
    
