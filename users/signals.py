from django.db.models.signals import post_save, post_delete

from django.dispatch import receiver

from django.contrib.auth.models import User

from .models import Profiles

from django.core.mail import send_mail

from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profiles.objects.create(
            user=user, 
            username= user.username, 
            email = user.email, 
            name = user.first_name,
        )

        subject = 'Welcome to WebProj'
        message = "Hi there!! \nCongratulations on Creating an account \nWe are Glad you're here"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )




def editUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        if profile.name:
            user.first_name = profile.name
        
        if profile.username:
            user.username = profile.username
        
        if profile.email:
            user.email = profile.email
        user.save()





def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass



post_save.connect(createProfile, sender=User)

post_delete.connect(deleteUser, sender=Profiles)


post_save.connect(editUser, sender=Profiles)