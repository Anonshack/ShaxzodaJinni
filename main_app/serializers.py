from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import InternshipCategory, Company, Internship, ContactMessage, InternshipApplication


class InternshipCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipCategory
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'label': _("Category Name")}
        }


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'label': _("Company Name")}
        }


class InternshipSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    category = InternshipCategorySerializer()

    class Meta:
        model = Internship
        fields = [
            'id',
            'image',
            'company',
            'category',
            'title',
            'published',
            'description',
            'full_description',
            'apply_url',
            'created_at',
        ]
        extra_kwargs = {
            'title': {'label': _("Internship Title")},
            'description': {'label': _("Short Description")},
            'full_description': {'label': _("Detailed Description")},
            'apply_url': {'label': _("Application Link")},
        }


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'message']
        extra_kwargs = {
            'first_name': {'label': _("First Name")},
            'last_name': {'label': _("Last Name")},
            'email': {'label': _("Email Address")},
            'phone_number': {'label': _("Phone Number")},
            'message': {'label': _("Message Content")},
        }


class InternshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipApplication
        fields = ['id', 'internship', 'file', 'additional_titles', 'description', 'status']
        read_only_fields = ['status']
        extra_kwargs = {
            'file': {'label': _("Uploaded File")},
            'description': {'label': _("Application Description")},
            'status': {'label': _("Application Status")},
        }

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url) if obj.file and request else None
