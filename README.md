## Its a task specific project :)

# Resume System Backend

Auto-generating resume builder that pulls from real achievements. Add an internship, get an updated resume instantly.

## flowchart

<img width="2505" height="4433" alt="Mermaid Chart - Create complex, visual diagrams with text -2025-10-21-193338" src="https://github.com/user-attachments/assets/cb159127-1a43-46de-811b-b13bcbd64719" />


## What It Does

Students manually update resumes after every achievement. This system automates it. Connect your activities (internships, courses, hackathons, projects) and your resume builds itself.

## Features

- **Auto-generation** - Resume updates when you add achievements
- **Smart skill extraction** - Pulls skills from everything, combines them
- **REST APIs** - Complete CRUD operations
- **JWT Auth** - Secure token-based authentication
- **Webhook ready** - External platforms can push data
- **Handles empty states** - Works even with no data

## Tech Stack

- Django 5.0 + Django REST Framework
- JWT authentication
- SQLite (PostgreSQL ready)
- Swagger documentation

## Quick Start
```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for API docs.

## Project Structure
```
api/
├── models.py       # Database structure
├── services.py     # Business logic (NEW!)
├── views.py        # API endpoints
├── serializers.py  # Data validation
└── urls.py         # Routing
```

Separated business logic into service layer instead of stuffing everything in models. Makes testing easier and code cleaner.

## API Overview
```
POST   /api/auth/register/        Register user
POST   /api/auth/login/           Get JWT token
GET    /api/resume/               Get auto-generated resume
POST   /api/internships/          Add internship
POST   /api/courses/              Add course
POST   /api/projects/             Add project
POST   /api/hackathons/           Add hackathon
POST   /api/webhook/achievement/  External platform webhook
```

## How Auto-Generation Works

Django signals detect when you add achievements. Triggers resume regeneration automatically. Extracts skills from all activities, removes duplicates, builds clean JSON structure.

## My Approach

Started with the database models - defined 6 models for users, achievements, and resumes. 

Separated business logic into a service layer. Created 4 service classes handling profiles, resume generation, achievements, and webhooks. This keeps code organized and testable.

Built REST APIs using DRF ViewSets. Added JWT for auth since it's stateless and works better for APIs.

Main challenge was handling empty data. Added checks so the system works even when users have no achievements yet - returns proper JSON with empty arrays.

The webhook endpoint lets external platforms push data directly. Validates incoming data and creates achievements automatically.

## Future Enhancements

### high_priority
- **PDF Export** - Convert JSON resume to downloadable PDF using ReportLab
- **Multiple Templates** - Add professional, creative, academic formats
- **AI Summary** - Use GPT to generate professional summaries from achievements
- **Email Notifications** - Alert users when resume updates

### medium_priority
- **Resume Analytics** - Track views, downloads, keyword matching
- **Version History** - Save and compare resume versions over time
- **LinkedIn Import** - Pull existing experience directly
- **Public Profiles** - Share resume via unique URL

### More Enhancement stuff
- **Skill Recommendations** - Suggest skills based on role/industry
- **Achievement Verification** - Verify certificates and achievements
- **Collaborative Editing** - Let mentors suggest improvements
- **ATS Optimization** - Score resume against job descriptions
- **Portfolio Integration** - Embed GitHub repos, live project demos

### Technical stuff
- **Caching** - Add Redis for faster resume generation
- **Rate Limiting** - Protect APIs from abuse
- **Comprehensive Tests** - Unit tests for services
- **Docker Setup** - Containerize for easy deployment
- **CI/CD Pipeline** - Automated testing and deployment

## Testing

Use Swagger UI at `http://127.0.0.1:8000/` to test all endpoints. 

Sample flow:
1. Register user
2. Login to get token
3. Add internship with token
4. Check `/api/resume/` - it updated automatically

## Deployment

Works with Heroku, Railway, AWS, or DigitalOcean. Just add PostgreSQL, set environment variables, and deploy.

## What's Different

Most resume builders need manual input every time. This one connects to real achievements and updates automatically. The webhook support means any platform can integrate - imagine Coursera auto-updating your resume when you finish a course.

The service layer architecture makes it production-ready. Can add features like PDF export or AI summaries without touching existing code.


## License

Created for trial task evaluation.
