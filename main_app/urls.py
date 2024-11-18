from django.urls import path
from .views import (
    ContactMessageView,
    InternshipListView,
    InternshipDetailView,
    InternshipSearchView,
    ApplyToInternshipView,
    AboutView,
    AdminAboutView,
    AdminApplicationView,
    UserApplicationsView,
    ChangeLanguageAPI,
)

urlpatterns = [
    path('contact/', ContactMessageView.as_view(), name='contact-message'),
    path('internships/', InternshipListView.as_view(), name='internship-list'),
    path('internships/<int:pk>/', InternshipDetailView.as_view(), name='internship-detail'),
    path('internships/search/', InternshipSearchView.as_view(), name='internship-search'),
    path('apply/', ApplyToInternshipView.as_view(), name='apply-to-internship'),
    path('about/', AboutView.as_view(), name='about-api'),
    path('my-applications/', UserApplicationsView.as_view(), name='user-applications'),

    # for admin
    path('admin/about/', AdminAboutView.as_view(), name='admin-about-api'),

    # Foydalanuvchi applicationlarini boshqarish
    path('applications/admin/', AdminApplicationView.as_view(), name='admin-applications'),
    path('applications/admin/<int:pk>/<str:action>/', AdminApplicationView.as_view(), name='admin-application-action'),

    # language
    path('change-language/', ChangeLanguageAPI.as_view(), name='change-language'),
]
