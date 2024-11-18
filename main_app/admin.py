from django.contrib import admin
from .models import InternshipCategory, Company, Internship, ContactMessage, InternshipApplication


@admin.register(InternshipCategory)
class InternshipCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'published', 'created_at')
    search_fields = ('title', 'company__name', 'category__name')
    list_filter = ('company', 'category', 'published')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'internship', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'internship__title')
