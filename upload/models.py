from django.db import models
from django.conf import settings
import os
import shutil


def folder_directory_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance.user.username, instance.folder_name, filename)


def file_directory_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance.user.username, instance.folder.folder_name, filename)


class Folder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=30, blank=False)
    about_file = models.CharField(max_length=1000)
    folder_image = models.FileField(upload_to=folder_directory_path)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.folder_name

    def __unicode__(self):
        return '%s' % self.folder_name

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.folder_image.name))
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, self.user.username, self.folder_name))
        super(Folder, self).delete(*args, **kwargs)


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=40, blank=False)
    file = models.FileField(upload_to=file_directory_path, default='Untitled')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.file_name

    def __unicode__(self):
        return '%s' % self.file.name

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(File, self).delete(*args, **kwargs)
