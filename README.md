# SocialNetwork Project

## Project Overview
SocialNetwork is a Django-based social networking platform where users can post articles, comment, like, and follow other users.

## Table of Contents
```
SocialNetwork/
├── accounts/               # Account-related app
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── managers.py
│   ├── migrations/
│   ├── models.py
│   ├── templates/accounts/
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── home/                   # Home page-related app
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── managers.py
│   ├── migrations/
│   ├── models.py
│   ├── templates/home/
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── manage.py               # Django management script
├── README.md               # Project documentation
├── SocialNetwork/          # Project settings and configurations
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
├── static/                 # Static files
│   ├── css/
│   └── js/
│       └── script.js
└── templates/              # Template files
    ├── include/
    └── shared/
```

## Development Environment Setup
1. Ensure Python and Django are installed on your system.
2. Clone the project to your local machine:
   ```
   git clone [Project URL]
   ```
3. Navigate to the project directory:
   ```
   cd SocialNetwork
   ```
4. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Run database migrations:
   ```
   python manage.py migrate
   ```
7. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```
8. Start the development server:
   ```
   python manage.py runserver
   ```
## Docker:
1. 
   ```
   docker compose up --build
   ```
2. 
   ```
   docker compose run python manage.py migrate
   ```


## Key Features
- User registration and authentication
- Article posting, editing, and deletion
- Commenting on articles with nested replies
- Liking articles
- Following and being followed by other users

## Model Descriptions
- `Post`: Represents user articles with fields such as title, content, and image.
- `Comment`: Represents comments on articles, supporting nested replies.
- `PostLike`: Records user likes for articles.
- `CustomUser`: Custom user model with fields like username, email, and profile picture.
- `Relation`: Records following relationships between users.

## View Descriptions
- `PostCreateView`: Handles the logic for creating articles.
- `PostDetailView`: Displays article details, including comments and likes.
- `PostEditView`: Handles the logic for editing articles.
- `LoginView`: Manages user login logic.

## Form Descriptions
- `PostForm`: Form for creating and editing articles.
- `CommentForm`: Form for submitting comments.
- `LoginForm`: Form for user login.

## Template Descriptions
- `post_edit.html`: Template for the article editing page.

## Deployment Recommendations
- Before deploying, ensure `DEBUG` is set to `False` and configure the production database and static file services.

## Contribution Guidelines
If you wish to contribute to the project, please follow these steps:
1. Fork the project.
2. Create a new branch.
3. Commit your changes.
4. Initiate a Pull Request.