from rest_framework import viewsets,status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters 
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Student
from .serializers import StudentSerializer
from rest_framework.exceptions import AuthenticationFailed
filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import Semester, Batch, Student, Routine, Subject, Registration, Result, Announcement
from .serializers import SemesterSerializer, BatchSerializer, StudentSerializer, RoutineSerializer, SubjectSerializer, RegistrationSerializer, ResultSerializer, AnnouncementSerializer,StudentCreateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from rest_framework import permissions
<<<<<<< HEAD
=======
from django.contrib.auth.hashers import check_password
>>>>>>> ec077f6 (update student login)
from user.models import User




class SemesterFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="start_date", lookup_expr='gte')  
    end_date = filters.DateFilter(field_name="end_date", lookup_expr='lte')  
    year = filters.NumberFilter(field_name="year", lookup_expr='exact') 

    class Meta:
        model = Semester
        fields = ['start_date', 'end_date', 'year']

class StudentFilter(filters.FilterSet):
    batch_name = filters.CharFilter(field_name="batch__name", lookup_expr='icontains')  
    student_id = filters.CharFilter(field_name="student_id", lookup_expr='exact')  

    class Meta:
        model = Student
        fields = ['batch_name', 'student_id']

class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)  
    filterset_class = SemesterFilter 
    search_fields = ['name', 'year']  
    ordering_fields = ['start_date', 'end_date', 'year']  
    ordering = ['start_date'] 

class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_fields = ['name']  
    search_fields = ['name'] 
    ordering_fields = ['name']
    ordering = ['name']

class StudentViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Student objects.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_serializer_class(self):
        """
        Use a different serializer for creating objects.
        """
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer

    def perform_create(self, serializer):
        """
        Save a new student instance.
        """
        serializer.save()

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """
        Retrieve the authenticated user's student profile.
        """
        student = self.queryset.filter(user=request.user).first()
        if not student:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(student)
        return Response(serializer.data)

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_fields = ['batch__name']  
    search_fields = ['batch__name']  
    ordering_fields = ['batch__name']
    ordering = ['batch__name']

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_fields = ['course_title', 'course_code']  
    search_fields = ['course_title', 'course_code']  
    ordering_fields = ['course_title', 'credit']
    ordering = ['course_title']

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_fields = ['student__student_id', 'semester__name'] 
    search_fields = ['student__user__first_name', 'student__user__last_name', 'semester__name']
    ordering_fields = ['semester__start_date', 'total_fee']
    ordering = ['semester__start_date']

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_fields = ['subject__course_title', 'exam_type'] 
    search_fields = ['subject__course_title', 'student__user__first_name', 'exam_type']
    ordering_fields = ['marks', 'exam_type']
    ordering = ['marks']

class AnnouncementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_fields = ['title', 'batch__name']  
    search_fields = ['title', 'batch__name']
    ordering_fields = ['title', 'batch__name']
    ordering = ['title']




class LoginAPIView(APIView):
    def post(self, request):
<<<<<<< HEAD
        username = request.data.get('username')
        password = request.data.get('password')

        print(f"Debug - Username: {username}, Password: {password}")  # Development only

        if not username or not password:
            raise AuthenticationFailed("Username and password are required.")

        # If username is email, fetch the corresponding username
        
        user = User.objects.filter(email=username).first()
        if user:
            username = user.username

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid username or password.")

        # Get or create token for the authenticated user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

    

=======
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')
            
            
            try:
               
                user = User.objects.get(username=username)
                
                
                student = user.student  
                
                
                if check_password(password, student.password):
                    login(request, user)  
                    return Response({
                        "message": "Login successful",
                        "user_id": user.id,
                        "username": user.username,
                        "role": "student"
                    }, status=200)
                else:
                    return Response({"error": "Invalid username or password"}, status=401)
            except User.DoesNotExist:
                return Response({"error": "Invalid username or password"}, status=401)
            except Student.DoesNotExist:
                return Response({"error": "Student record not found"}, status=404)
        return Response(serializer.errors, status=400)
>>>>>>> ec077f6 (update student login)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Check if old password is correct
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if new passwords match
        if new_password != confirm_password:
            return Response({"error": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate new password
        try:
            validate_password(new_password, user)
        except Exception as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        Student.set_password(new_password)
        Student.save()

        # Update last login (optional)
        update_last_login(None, user)

        return Response({"success": "Password changed successfully."}, status=status.HTTP_200_OK)