from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class InternshipCategory(models.Model):
    name = models.CharField(_("Name"), max_length=20)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name


class Internship(models.Model):
    image = models.ImageField(_("Image"), upload_to='internships/', blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("Company"))
    category = models.ForeignKey(InternshipCategory, on_delete=models.CASCADE, verbose_name=_("Category"))
    title = models.CharField(_("Title"), max_length=255)
    published = models.DateField(_("Published Date"), null=True, blank=True)
    description = models.TextField(_("Description"))
    full_description = models.TextField(_("Full Description"))
    apply_url = models.URLField(_("Apply URL"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email"))
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class InternshipApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name=_("User"))
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='applications', verbose_name=_("Internship"))
    file = models.FileField(_("File"), upload_to='apply/', max_length=255)
    additional_titles = models.JSONField(_("Additional Titles"), default=dict)
    description = models.TextField(_("Description"), blank=True, null=True)
    status = models.CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(_("Applied At"), auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.internship.title} ({self.status})"
