from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import activate
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Internship, ContactMessage, InternshipApplication
from .serializers import (
    InternshipSerializer,
    ContactMessageSerializer,
    InternshipApplicationSerializer,
)
from django.conf import settings


class AboutView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        internship_count = Internship.objects.count()
        application_count = InternshipApplication.objects.count()
        user_count = User.objects.count()

        return Response({
            'internship_count': internship_count,
            'application_count': application_count,
            'user_count': user_count,
        })


class ContactMessageView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        messages = ContactMessage.objects.all()
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)


class InternshipListView(ListAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class InternshipDetailView(RetrieveAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class InternshipSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        category = request.query_params.get('category', None)
        company = request.query_params.get('company', None)
        internships = Internship.objects.all()

        if query:
            internships = internships.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        if category:
            internships = internships.filter(category__name__icontains=category)
        if company:
            internships = internships.filter(company__name__icontains=company)

        serializer = InternshipSerializer(internships, many=True)
        return Response(serializer.data)


class ApplyToInternshipView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InternshipApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Application submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminApplicationView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        applications = InternshipApplication.objects.filter(status='pending')
        serializer = InternshipApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, action=None):
        try:
            application = InternshipApplication.objects.get(pk=pk)
        except InternshipApplication.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
        if action == 'approve':
            application.status = 'approved'
            application.save()
            return Response({"status": "Tasdiqlangan"}, status=status.HTTP_200_OK)
        elif action == 'reject':
            application.status = 'rejected'
            application.save()
            return Response({"status": "Rad etilgan"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action. Use 'approve' or 'reject'."},
                            status=status.HTTP_400_BAD_REQUEST)


class AdminAboutView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        internship_count = Internship.objects.count()
        application_count = InternshipApplication.objects.count()
        user_count = User.objects.count()

        return Response({
            'internship_count': internship_count,
            'application_count': application_count,
            'user_count': user_count,
        })


class UserApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        applications = InternshipApplication.objects.filter(user=user)
        serializer = InternshipApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# language
class ChangeLanguageAPI(APIView):
    def post(self, request):
        language = request.data.get('language', None)
        if language not in dict(settings.LANGUAGES):
            return Response(
                {"error": "Til noto'g'ri yoki qo'llab-quvvatlanmaydi"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        activate(language)
        request.session[settings.LANGUAGE_COOKIE_NAME] = language
        return Response(
            {"message": f"Til muvaffaqiyatli {language} ga o'zgartirildi"},
            status=status.HTTP_200_OK,
        )

