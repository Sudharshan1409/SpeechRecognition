"""
Models.py includes the database structure of the application.
"""

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_delete,post_save,pre_save
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="users/profile_pics/", blank = True)
    gender = models.CharField(max_length=10, choices=(('Male','Male'),('Female','Female')))
    age = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('users:home',kwargs = {'pk':self.pk})

    def __str__(self):
        return f"{self.user.username.capitalize()} Profile"

@receiver(post_delete, sender=UserProfile)
def submission_delete(sender, instance, **kwargs):
    """
    This function is used to delete attachments when a file object is deleted.
    Django does not do this automatically.
    """
    instance.profile_pic.delete(False)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
        print('profile created')

@receiver(post_save,sender=User)
def update_profile(sender,instance,created, **kwargs):
    if not created:
        instance.userprofile.save()
        print('profile updated')

@receiver(post_delete, sender=User)
def delete_user_profile(sender,instance, **kwargs):
    instance.userprofile.delete()


class FileModel(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name = 'files', blank=True, null=True)
    file = models.FileField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.FilePathField(path=settings.MEDIA_ROOT, default=settings.MEDIA_ROOT)

    class Meta:
        unique_together = ['file', 'path']

    def filename(self):
        return os.path.basename(self.file.name)


@receiver(post_delete, sender=FileModel)
def submission_delete(sender, instance, **kwargs):
    """
    This function is used to delete attachments when a file object is deleted.
    Django does not do this automatically.
    """
    instance.file.delete(False)
