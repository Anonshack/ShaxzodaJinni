from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import activate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
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
    """
    API endpoint for managing contact messages.
    """

    @swagger_auto_schema(
        operation_description="Retrieve a list of all contact messages or a single message by ID.",
        responses={
            200: ContactMessageSerializer(many=True),
            404: "Message not found."
        },
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_QUERY,
                description="Optional ID of a specific message to retrieve.",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, pk=None):
        """
        Retrieve one or all messages.
        """
        if pk:
            try:
                message = ContactMessage.objects.get(pk=pk)
                serializer = ContactMessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ContactMessage.DoesNotExist:
                return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            messages = ContactMessage.objects.all()
            serializer = ContactMessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new contact message.",
        request_body=ContactMessageSerializer,
        responses={
            201: openapi.Response(
                "Message created successfully!",
                ContactMessageSerializer
            ),
            400: "Bad Request",
        },
    )
    def post(self, request):
        """
        Create a new contact message.
        """
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a contact message by ID.",
        request_body=ContactMessageSerializer,
        responses={
            200: "Message updated successfully!",
            400: "Bad Request",
            404: "Message not found."
        }
    )
    def put(self, request, pk):
        """
        Update an entire contact message.
        """
        try:
            message = ContactMessage.objects.get(pk=pk)
        except ContactMessage.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactMessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message updated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a contact message by ID.",
        request_body=ContactMessageSerializer,
        responses={
            200: "Message partially updated successfully!",
            400: "Bad Request",
            404: "Message not found."
        }
    )
    def patch(self, request, pk):
        """
        Partially update a contact message.
        """
        try:
            message = ContactMessage.objects.get(pk=pk)
        except ContactMessage.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactMessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message partially updated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a contact message by ID.",
        responses={
            204: "Message deleted successfully!",
            404: "Message not found."
        }
    )
    def delete(self, request, pk):
        """
        Delete a contact message by ID.
        """
        try:
            message = ContactMessage.objects.get(pk=pk)
            message.delete()
            return Response({"message": "Message deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        except ContactMessage.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)


class InternshipListView(ListCreateAPIView):
    """
    List all internships or create a new one (Admins only for creating).
    """
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all internships.",
        responses={
            200: InternshipSerializer(many=True)
        },
    )
    def get(self, request, *args, **kwargs):
        """
        List all internships.
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new internship (Admins only).",
        request_body=InternshipSerializer,
        responses={
            201: InternshipSerializer,
            400: "Bad Request"
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new internship. Only admins can create.
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super().post(request, *args, **kwargs)


class InternshipDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an internship (Admins only for update/delete).
    """
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific internship by ID.",
        responses={
            200: InternshipSerializer,
            404: "Not Found"
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve an internship by ID.
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an internship (Admins only).",
        request_body=InternshipSerializer,
        responses={
            200: InternshipSerializer,
            400: "Bad Request",
            404: "Not Found"
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Update an internship. Only admins can update.
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update an internship (Admins only).",
        request_body=InternshipSerializer,
        responses={
            200: InternshipSerializer,
            400: "Bad Request",
            404: "Not Found"
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        Partially update an internship. Only admins can update.
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an internship (Admins only).",
        responses={
            204: "No Content",
            404: "Not Found"
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete an internship. Only admins can delete.
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super().delete(request, *args, **kwargs)


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
    """
    Admin view for managing internship applications.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all pending applications.",
        responses={200: InternshipApplicationSerializer(many=True)}
    )
    def get(self, request):
        """
        Get all pending internship applications.
        """
        applications = InternshipApplication.objects.filter(status='pending')
        serializer = InternshipApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Approve or reject a specific application by ID.",
        manual_parameters=[
            openapi.Parameter(
                'action',
                openapi.IN_QUERY,
                description="Action to perform ('approve' or 'reject').",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Application status updated."),
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def post(self, request, pk):
        """
        Approve or reject an application. Requires 'approve' or 'reject' as action in query params.
        """
        action = request.query_params.get('action', None)

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
            return Response(
                {"error": "Invalid action. Use 'approve' or 'reject'."},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="Delete a specific application by ID.",
        responses={
            204: "Application deleted successfully.",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        """
        Delete a specific application by ID.
        """
        try:
            application = InternshipApplication.objects.get(pk=pk)
            application.delete()
            return Response({"message": "Application deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except InternshipApplication.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)


class AdminAboutView(APIView):
    """
    API endpoint for admin statistics and managing about information.
    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Retrieve admin statistics such as internship count, application count, and user count.",
        responses={
            200: openapi.Response(
                description="Statistics retrieved successfully.",
                examples={
                    "application/json": {
                        "internship_count": 10,
                        "application_count": 50,
                        "user_count": 100
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve admin statistics.
        """
        internship_count = Internship.objects.count()
        application_count = InternshipApplication.objects.count()
        user_count = User.objects.count()

        return Response({
            'internship_count': internship_count,
            'application_count': application_count,
            'user_count': user_count,
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new admin about record (not implemented, for extension purposes).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'internship_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of internships"),
                'application_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of applications"),
                'user_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of users"),
            },
        ),
        responses={
            201: "New about record created successfully.",
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        """
        (Optional) Create a new about record. Placeholder for future use.
        """
        data = request.data
        return Response({"message": "Record creation is not implemented."}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update the admin about statistics (placeholder, not implemented).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'internship_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of internships"),
                'application_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of applications"),
                'user_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of users"),
            },
        ),
        responses={
            200: "Statistics updated successfully.",
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, *args, **kwargs):
        """
        (Optional) Update the about statistics. Placeholder for future use.
        """
        return Response({"message": "Update is not implemented."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Partially update admin statistics (placeholder, not implemented).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'internship_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of internships"),
                'application_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of applications"),
                'user_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of users"),
            },
        ),
        responses={
            200: "Statistics partially updated successfully.",
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def patch(self, request, *args, **kwargs):
        """
        (Optional) Partially update the about statistics. Placeholder for future use.
        """
        return Response({"message": "Partial update is not implemented."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete admin about statistics (placeholder, not implemented).",
        responses={
            204: "Statistics deleted successfully.",
            404: "Not Found"
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        (Optional) Delete about statistics. Placeholder for future use.
        """
        return Response({"message": "Delete is not implemented."}, status=status.HTTP_204_NO_CONTENT)


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

