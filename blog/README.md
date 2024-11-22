### Django Blog Project

A blogging platform built using Django that allows users to create, edit, and comment on blog posts. This project also includes REST API support for managing blog data programmatically.

### Features

User authentication (registration, login, and logout).
Create, update, delete blog posts.
Add comments to blog posts.
REST API endpoints for blog operations.
Responsive design using HTML and CSS.

### Project Structure

blog_project/
├── blog/                  # Main Django app containing blog logic
│   ├── migrations/        # Database migrations
│   ├── models.py          # Database models
│   ├── serializers.py     # Serializer classes for API endpoints
│   ├── static/            # Static files (CSS, JS)
│   ├── templates/         # HTML templates for views
│   ├── tests.py           # Unit tests for the app
│   └── views.py           # HTTP request handlers
├── blog_project/          # Project settings and configurations
│   ├── _init_.py
│   ├── settings.py        # Django settings (e.g., database, installed apps)
│   ├── urls.py            # Root URL configurations
│   ├── wsgi.py            # WSGI configuration for deployment
│   └── asgi.py            # ASGI configuration for async support
├── manage.py              # Django management utility
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation


### Requirements

Python 3.8 or higher
Django 5.1
MySQL 8.0 or higher (or any other supported database)
Git (for version control)

### Installation

1. Clone the repository:
git clone https://github.com/yourusername/django-blog.git

2. Navigate into the project directory:
cd django-blog

3. Create a virtual environment (recommended):
For Windows:
python -m venv venv
venv\Scripts\activate

For macOS/Linux:
python3 -m venv venv
source venv/bin/activate

4. Install required dependencies:
pip install -r requirements.txt

5. Set up the database:
Configure your database credentials in blog_project/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blogdb',
        'USER': 'yourusername',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

6. Apply migrations:
python manage.py migrate

7. Create a superuser (for admin access):
python manage.py createsuperuser

8. Run the development server:
python manage.py runserver

## API Endpoints
The following API endpoints are available in this project:

### Blog Posts
- *GET* /api/posts/  
  - Description: Retrieve a list of all blog posts.  
  - Response:
    json
    [
      {
        "id": 1,
        "title": "Sample Post",
        "content": "This is the content of the sample post.",
        "author": "User1",
        "created_at": "2024-11-22T12:00:00Z"
      }
    ]
      
- *GET* /api/posts/<id>/  
  - Description: Retrieve details of a single blog post by ID.  
  - Response:
    json
    {
      "id": 1,
      "title": "Sample Post",
      "content": "This is the content of the sample post.",
      "author": "User1",
      "created_at": "2024-11-22T12:00:00Z"
    }
    
- *POST* /api/posts/  
  - Description: Create a new blog post.  
  - Request Body:
    json
    {
      "title": "New Post",
      "content": "This is the content of the new post."
    }
    
  - Response:
    json
    {
      "id": 2,
      "title": "New Post",
      "content": "This is the content of the new post.",
      "author": "User1",
      "created_at": "2024-11-22T12:10:00Z"
    }
    
### Comments
- *GET* /api/posts/<post_id>/comments/  
  - Description: Retrieve all comments for a specific blog post.  
  - Response:
    json
    [
      {
        "id": 1,
        "content": "This is a comment.",
        "author": "User2",
        "created_at": "2024-11-22T12:30:00Z"
      }
    ]
    

- *POST* /api/posts/<post_id>/comments/  
  - Description: Add a comment to a specific blog post.  
  - Request Body:
    json
    {
      "content": "This is a new comment."
    }
    
  - Response:
    json
    {
      "id": 2,
      "content": "This is a new comment.",
      "author": "User1",
      "created_at": "2024-11-22T12:45:00Z"
    }
    
### User Authentication
- *POST* /api/register/  
  - Description: Register a new user.  
  - Request Body:
    json
    {
      "username": "newuser",
      "password": "password123"
    }
    
  - Response:
    json
    {
      "id": 1,
      "username": "newuser"
    }
    
- *POST* /api/login/  
  - Description: Authenticate a user and retrieve a token.  
  - Request Body:
    json
    {
      "username": "existinguser",
      "password": "password123"
    }
    
  - Response:
    json
    {
      "token": "abc123xyz"
    }
    
### Testing
To run the tests, use the following command:  python manage.py test

### Documentation
1. Browsable API: Once the server is running, navigate to /api/ to explore the REST API using Django REST Framework's browsable interface.
2. Swagger/Postman:

Use Swagger or Postman to document and test the API. Import the provided Postman collection or Swagger YAML file (if available).

### Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature).
5. Open a pull request.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
