from django.contrib.auth.models import User
from .models import UserProfile, Resume, Internship, Course, Hackathon, Project


class UserProfileService:
    """Service for managing user profiles"""
    
    @staticmethod
    def create_user_profile(user):
        """Create a new user profile"""
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile
    
    @staticmethod
    def get_or_create_profile(user):
        """Get existing profile or create if doesn't exist"""
        try:
            return user.profile
        except UserProfile.DoesNotExist:
            return UserProfileService.create_user_profile(user)
    
    @staticmethod
    def update_profile(user, **kwargs):
        """Update user profile with provided data"""
        profile = UserProfileService.get_or_create_profile(user)
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        profile.save()
        return profile


class ResumeService:
    """Service for managing resume operations"""
    
    @staticmethod
    def create_resume(user):
        """Create a new resume for user"""
        resume, created = Resume.objects.get_or_create(user=user)
        if created:
            ResumeService.generate_resume(resume)
        return resume
    
    @staticmethod
    def get_or_create_resume(user):
        """Get existing resume or create if doesn't exist"""
        try:
            return user.resume
        except Resume.DoesNotExist:
            return ResumeService.create_resume(user)
    
    @staticmethod
    def extract_skills_from_achievements(user):
        """
        Extract and aggregate all skills from user's achievements
        Returns a sorted list of unique skills
        """
        all_skills = set()
        
        
        for internship in user.internships.all():
            if internship.skills_used:
                skills = [s.strip() for s in internship.skills_used.split(',') if s.strip()]
                all_skills.update(skills)
        
        
        for course in user.courses.all():
            if course.skills_learned:
                skills = [s.strip() for s in course.skills_learned.split(',') if s.strip()]
                all_skills.update(skills)
        
        
        for hackathon in user.hackathons.all():
            if hackathon.tech_stack:
                skills = [s.strip() for s in hackathon.tech_stack.split(',') if s.strip()]
                all_skills.update(skills)
        
        
        for project in user.projects.all():
            if project.tech_stack:
                skills = [s.strip() for s in project.tech_stack.split(',') if s.strip()]
                all_skills.update(skills)
        
    
        all_skills = {skill for skill in all_skills if skill}
        return sorted(list(all_skills))
    
    @staticmethod
    def build_personal_info(user, profile):
        """Build personal information section of resume"""
        full_name = f"{user.first_name} {user.last_name}".strip()
        
        return {
            "name": full_name or user.username,
            "email": user.email,
            "phone": profile.phone or "",
            "linkedin": profile.linkedin or "",
            "github": profile.github or "",
            "location": profile.location or "",
            "bio": profile.bio or "No bio available"
        }
    
    @staticmethod
    def build_internships_section(user):
        """Build internships section of resume"""
        if not user.internships.exists():
            return []
        
        return [
            {
                "company": i.company,
                "role": i.role,
                "start_date": str(i.start_date),
                "end_date": str(i.end_date) if i.end_date else "Present",
                "description": i.description,
                "skills": i.skills_used,
                "location": i.location,
                "is_current": i.is_current
            }
            for i in user.internships.all()
        ]
    
    @staticmethod
    def build_courses_section(user):
        """Build courses section of resume"""
        if not user.courses.exists():
            return []
        
        return [
            {
                "platform": c.platform,
                "title": c.title,
                "completion_date": str(c.completion_date),
                "certificate_url": c.certificate_url or "",
                "skills": c.skills_learned,
                "duration_hours": c.duration_hours
            }
            for c in user.courses.all()
        ]
    
    @staticmethod
    def build_hackathons_section(user):
        """Build hackathons section of resume"""
        if not user.hackathons.exists():
            return []
        
        return [
            {
                "name": h.name,
                "organizer": h.organizer,
                "date": str(h.date),
                "rank": h.rank or "Participant",
                "project_name": h.project_name,
                "project_description": h.project_description,
                "project_link": h.project_link or "",
                "tech_stack": h.tech_stack
            }
            for h in user.hackathons.all()
        ]
    
    @staticmethod
    def build_projects_section(user):
        """Build projects section of resume"""
        if not user.projects.exists():
            return []
        
        return [
            {
                "title": p.title,
                "description": p.description,
                "tech_stack": p.tech_stack,
                "github_link": p.github_link or "",
                "live_link": p.live_link or "",
                "start_date": str(p.start_date),
                "end_date": str(p.end_date) if p.end_date else "Ongoing",
                "is_ongoing": p.is_ongoing
            }
            for p in user.projects.all()
        ]
    
    @staticmethod
    def generate_resume(resume):
        """
        main function to generate complete resume from user's achievements
        """
        user = resume.user
        
        
        profile = UserProfileService.get_or_create_profile(user)
        
       
        all_skills = ResumeService.extract_skills_from_achievements(user)
        
        
        resume_data = {
            "personal_info": ResumeService.build_personal_info(user, profile),
            "skills": all_skills,
            "internships": ResumeService.build_internships_section(user),
            "courses": ResumeService.build_courses_section(user),
            "hackathons": ResumeService.build_hackathons_section(user),
            "projects": ResumeService.build_projects_section(user),
            "summary": ResumeService.generate_summary(user, all_skills)
        }
        
        
        resume.resume_data = resume_data
        resume.save()
        
        return resume
    
    @staticmethod
    def generate_summary(user, skills):
        """
        Generate a professional summary based on user's achievements
        This can be enhanced with AI in the future
        """
        total_internships = user.internships.count()
        total_courses = user.courses.count()
        total_hackathons = user.hackathons.count()
        total_projects = user.projects.count()
        
        if not any([total_internships, total_courses, total_hackathons, total_projects]):
            return "Aspiring professional looking to build a career in technology."
        
        summary_parts = []
        
        
        if total_internships > 0:
            summary_parts.append(f"Experienced professional with {total_internships} internship(s)")
        
        
        if len(skills) > 0:
            top_skills = ', '.join(skills[:5]) #only 5 
            summary_parts.append(f"skilled in {top_skills}")
        
    
        if total_projects > 0:
            summary_parts.append(f"with {total_projects} project(s) completed")
        
        
        if total_hackathons > 0:
            summary_parts.append(f"and {total_hackathons} hackathon participation(s)")
        
        summary = ". ".join(summary_parts) + "."
        return summary.capitalize()
    
    @staticmethod
    def regenerate_resume(user):
        """Manually trigger resume regeneration"""
        resume = ResumeService.get_or_create_resume(user)
        return ResumeService.generate_resume(resume)


class AchievementService:
    """Service for managing achievements"""
    
    @staticmethod
    def add_internship(user, data):
        """Add internship and trigger resume update"""
        internship = Internship.objects.create(user=user, **data)
        ResumeService.regenerate_resume(user)
        return internship
    
    @staticmethod
    def add_course(user, data):
        """Add course and trigger resume update"""
        course = Course.objects.create(user=user, **data)
        ResumeService.regenerate_resume(user)
        return course
    
    @staticmethod
    def add_hackathon(user, data):
        """Add hackathon and trigger resume update"""
        hackathon = Hackathon.objects.create(user=user, **data)
        ResumeService.regenerate_resume(user)
        return hackathon
    
    @staticmethod
    def add_project(user, data):
        """Add project and trigger resume update"""
        project = Project.objects.create(user=user, **data)
        ResumeService.regenerate_resume(user)
        return project
    
    @staticmethod
    def get_user_statistics(user):
        """Get statistics of user's achievements"""
        resume = ResumeService.get_or_create_resume(user)
        
        return {
            'total_internships': user.internships.count(),
            'total_courses': user.courses.count(),
            'total_hackathons': user.hackathons.count(),
            'total_projects': user.projects.count(),
            'total_skills': len(resume.resume_data.get('skills', [])),
            'resume_last_updated': resume.last_generated,
            'has_complete_profile': all([
                user.first_name,
                user.last_name,
                user.email,
                hasattr(user, 'profile') and user.profile.phone
            ])
        }


class WebhookService:
    """Service for handling webhook integrations"""
    
    @staticmethod
    def process_achievement_webhook(user_email, achievement_type, data):
        """
        Process achievement data received from external platforms
        Returns: (success: bool, message: str, achievement: object or None)
        """
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return False, "User not found", None
        
        achievement = None
        
        if achievement_type == 'internship':
            achievement = AchievementService.add_internship(user, data)
            message = "Internship added successfully"
        
        elif achievement_type == 'course':
            achievement = AchievementService.add_course(user, data)
            message = "Course added successfully"
        
        elif achievement_type == 'hackathon':
            achievement = AchievementService.add_hackathon(user, data)
            message = "Hackathon added successfully"
        
        elif achievement_type == 'project':
            achievement = AchievementService.add_project(user, data)
            message = "Project added successfully"
        
        else:
            return False, "Invalid achievement type", None
        
        return True, message, achievement