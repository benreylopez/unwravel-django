from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from accounts.managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):

    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, db_index=True)
    brasize = models.CharField(max_length=255, null=True, blank=True)
    pantysize = models.CharField(max_length=255, null=True, blank=True)
    bottomsize = models.CharField(max_length=255, null=True, blank=True)
    topsize = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField('active', default=True)

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    REQUIRED_FIELDS = ['firstname', 'lastname']
    USERNAME_FIELD = 'email'

    objects = AccountManager()

    @property
    def is_staff(self):
        return self.is_superuser



