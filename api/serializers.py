from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Internship, Course, Hackathon, Project, Resume

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'phone', 'bio', 'linkedin', 'github', 'location', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ['id', 'company', 'role', 'start_date', 'end_date', 'description', 
                  'skills_used', 'location', 'is_current', 'created_at']
        read_only_fields = ['id', 'created_at']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'platform', 'title', 'completion_date', 'certificate_url', 
                  'skills_learned', 'duration_hours', 'created_at']
        read_only_fields = ['id', 'created_at']

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ['id', 'name', 'organizer', 'date', 'rank', 'project_name', 
                  'project_description', 'project_link', 'tech_stack', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tech_stack', 'github_link', 
                  'live_link', 'start_date', 'end_date', 'is_ongoing', 'created_at']
        read_only_fields = ['id', 'created_at']

class ResumeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Resume
        fields = ['user', 'resume_data', 'last_generated', 'template_type']
        read_only_fields = ['last_generated']