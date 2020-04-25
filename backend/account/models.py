from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("Name"), unique=True, max_length=30, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=30)
    email = models.EmailField(_("Email"), unique=True, blank=True, null=True)
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'last_name']

    objects = UserManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _("user")
        verbose_name_plural = _("users")