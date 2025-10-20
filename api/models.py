from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Internship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='internships')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    skills_used = models.CharField(max_length=500, help_text="Comma separated skills")
    location = models.CharField(max_length=100, blank=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} at {self.company}"

    class Meta:
        ordering = ['-start_date']

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    platform = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    completion_date = models.DateField()
    certificate_url = models.URLField(blank=True)
    skills_learned = models.CharField(max_length=500, help_text="Comma separated skills")
    duration_hours = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} on {self.platform}"

    class Meta:
        ordering = ['-completion_date']

class Hackathon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hackathons')
    name = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200)
    date = models.DateField()
    rank = models.CharField(max_length=50, blank=True)
    project_name = models.CharField(max_length=200)
    project_description = models.TextField()
    project_link = models.URLField(blank=True)
    tech_stack = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.project_name}"

    class Meta:
        ordering = ['-date']

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500)
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_ongoing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    resume_data = models.JSONField(default=dict)
    last_generated = models.DateTimeField(auto_now=True)
    template_type = models.CharField(max_length=50, default='modern')

    def __str__(self):
        return f"Resume of {self.user.username}"

    def generate_resume(self):
        """
        Auto-generate resume from user's achievements
        Note: Actual logic is in services.py for better separation of concerns
        """
        from .services import ResumeService
        return ResumeService.generate_resume(self)

# Signal to auto-create UserProfile and Resume when User is created
@receiver(post_save, sender=User)
def create_user_profile_and_resume(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Resume.objects.create(user=instance)

# Signals to auto-update resume when achievements are added/updated
@receiver(post_save, sender=Internship)
@receiver(post_save, sender=Course)
@receiver(post_save, sender=Hackathon)
@receiver(post_save, sender=Project)
def update_resume(sender, instance, **kwargs):
    try:
        resume = instance.user.resume
        resume.generate_resume()
    except Resume.DoesNotExist:
        Resume.objects.create(user=instance.user)
        instance.user.resume.generate_resume()