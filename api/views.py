from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import UserProfile, Internship, Course, Hackathon, Project, Resume
from .serializers import (
    UserSerializer, UserProfileSerializer, UserRegistrationSerializer,
    InternshipSerializer, CourseSerializer, HackathonSerializer, 
    ProjectSerializer, ResumeSerializer
)
from .services import (
    UserProfileService, ResumeService, AchievementService, WebhookService
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user and return JWT tokens"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def get_object(self):
        return self.request.user.profile

class InternshipViewSet(viewsets.ModelViewSet):
    serializer_class = InternshipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Internship.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HackathonViewSet(viewsets.ModelViewSet):
    serializer_class = HackathonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Hackathon.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    def get_object(self):
        return self.request.user.resume
    
    @action(detail=False, methods=['post'])
    def regenerate(self, request):
        """Manually trigger resume regeneration"""
        resume = request.user.resume
        resume.generate_resume()
        serializer = self.get_serializer(resume)
        return Response({
            'message': 'Resume regenerated successfully',
            'resume': serializer.data
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def webhook_achievement(request):
    """
    Webhook endpoint to receive achievements from external platforms
    Expected format:
    {
        "user_email": "user@example.com",
        "type": "internship|course|hackathon|project",
        "data": {...}
    }
    """
    user_email = request.data.get('user_email')
    achievement_type = request.data.get('type')
    data = request.data.get('data')
    
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Process based on type
    if achievement_type == 'internship':
        serializer = InternshipSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'message': 'Internship added successfully'}, status=status.HTTP_201_CREATED)
    
    elif achievement_type == 'course':
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'message': 'Course added successfully'}, status=status.HTTP_201_CREATED)
    
    elif achievement_type == 'hackathon':
        serializer = HackathonSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'message': 'Hackathon added successfully'}, status=status.HTTP_201_CREATED)
    
    elif achievement_type == 'project':
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'message': 'Project added successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'error': 'Invalid achievement type'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get user's achievement statistics"""
    user = request.user
    stats = {
        'total_internships': user.internships.count(),
        'total_courses': user.courses.count(),
        'total_hackathons': user.hackathons.count(),
        'total_projects': user.projects.count(),
        'resume_last_updated': user.resume.last_generated,
        'total_skills': len(user.resume.resume_data.get('skills', []))
    }
    return Response(stats)