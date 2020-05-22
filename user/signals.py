from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, OthersProfiles, Gallery
from match.models import User_Answer

from django.conf import settings
import os

# FOR PROFILE
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()


# For USER_ANSWER
@receiver(post_save, sender=User)
def create_user_answer(sender, instance, created, **kwargs):
	if created:
		User_Answer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_answer(sender, instance, **kwargs):
	instance.user_answer.save()

#For OthersProfiles
@receiver(post_save, sender=User)
def create_othersprofiles(sender, instance, created, **kwargs):
	if created:
		OthersProfiles.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_othersprofiles(sender, instance, **kwargs):
	instance.othersprofiles.save()


@receiver(post_save, sender=User)
def create_directory(sender, instance, created, **kwargs):
	if created:
		path = settings.MEDIA_ROOT
		path = f'{path}/user_{instance.id}/'
		os.makedirs(path)


@receiver(post_save, sender=User)
def create_gallery(sender, instance, created, **kwargs):
	if created:
		Gallery.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_gallery(sender, instance, **kwargs):
	instance.gallery.save()

  
# @receiver(post_save, sender=Gallery)
# def image_directory_path(sender, instance, created,**kwargs):
# 	if created:
# 		imagefile = instance.gallery_image
# 		old_name = imagefile.name
# 		if not old_name:
# 			return
# 		new_name = os.path.basename(old_name)
# 		new_path = os.path.join(settings.MEDIA_ROOT,sender.image_directory_path(instance, new_name))
# 		if not os.path.exists(new_path):
# 			os.makedirs(os.path.dirname(new_path))
# 		instance.gallery_image.name=sender.image_directory_path(instance, new_name)
# 		instance.save()