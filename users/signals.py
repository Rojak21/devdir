from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from .models import Profile 
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


@receiver(post_save, sender=Profile)
def profileUpdated(sender, instance, created, **kwargs):
    print("Profile saved")
    print('instance : ', instance)
    print('created : ', created)

# post_save.connect(profileUpdated, sender=Profile)
@receiver(post_save, sender=User)
def createProfile(sender,instance,created,**kwargs):
    user=instance
    if created:
        Profile.objects.create(user=user,username=user.username,name=user.first_name,email=user.email)
        subject="welcome to devdir"
        message="Thanks for joining our community"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        User=instance.user
        User.delete()
    except:
        pass

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile=instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
        