# Connectly API

API for social media-like platform with posts, likes, comments, Google OAuth login, and news feed.

## Features
- CRUD for posts and comments
- Like toggle on posts
- Google OAuth login (browser + API)
- News feed with sorting (newest first) and pagination

## Endpoints
- POST /posts/ - Create post
- POST /posts/<id>/like/ - Toggle like
- POST /posts/<id>/comment/ - Add comment
- GET /feed/?page=1 - News feed (paginated)

## Testing
See `/testing-evidence/` folder for Postman screenshots.

## Setup
1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py runserver`
