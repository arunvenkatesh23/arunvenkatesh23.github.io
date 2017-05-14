from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.conf import settings
import os
import shutil


def folder_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.username, filename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, blank=False)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_of_birth = models.DateField(blank=False)
    address = models.CharField(max_length=300, blank=False)
    city = models.CharField(max_length=30, blank=False)
    state = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=30, blank=False)
    mobile = models.CharField(max_length=10, blank=False)
    avatar = models.FileField(upload_to=folder_directory_path, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=300, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth', 'address', 'city', 'state', 'country',
                       'mobile', 'avatar', 'is_active', 'is_superuser', 'is_staff']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.avatar.name))
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, self.username))
        super(User, self).delete(*args, **kwargs)
