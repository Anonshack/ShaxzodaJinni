from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,  # Use the 'User' alias instead of calling get_user_model() again
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_("User")
    )
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)
    email = models.EmailField(_("Email"))
    profile_picture = models.ImageField(
        _("Profile Picture"), upload_to='profile_pics/', blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.email}'s Profile"

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")


class CustomUser(AbstractUser):
    email = models.EmailField(_("Email Address"), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        verbose_name=_("Groups")
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
        verbose_name=_("User Permissions")
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")
