# Connectly API - Terminal Assessment

A social media backend API developed for **MO-IT152 Integrative Programming and Technologies** at Mapua-Malayan Digital College.

## Project Overview

This API supports a social media platform called **Connectly** with full CRUD operations, authentication, and advanced features implemented in the Terminal Assessment.

## Features Implemented

### Milestone 2
- User registration & Google OAuth login
- Post creation, likes, and comments
- News Feed with pagination and sorting

### Terminal Assessment (Final Requirements)
- **Privacy Settings**: Posts can be set as `public` or `private`
- **Role-Based Access Control (RBAC)**: `admin` and `user` roles
- Only `admin` users can delete posts and comments
- Private posts are visible **only to the owner**
- News Feed respects privacy rules + pagination (10 posts per page)

## Technologies Used
- Django 6.0 + Django REST Framework
- SimpleJWT Authentication
- Allauth with Google OAuth2
- Custom User Model with Role field

## Important Endpoints

| Feature                    | Method | Endpoint                        | Notes                          |
|---------------------------|--------|----------------------------------|--------------------------------|
| Create Post               | POST   | `/posts/`                        | Supports privacy field         |
| View Single Post          | GET    | `/posts/<id>/`                   | Privacy enforced               |
| Delete Post               | DELETE | `/posts/<id>/delete/`            | Admin only                     |
| News Feed                 | GET    | `/feed/?page=1`                  | Privacy + Pagination           |
| Add Comment               | POST   | `/posts/<id>/comment/`           | Authenticated users            |

## Repository Structure
- `models.py` – Custom User, Post (with privacy), Comment
- `views.py` – Privacy checks, RBAC logic, Feed with filtering
- `serializers.py` – Updated with role and privacy fields
- `urls.py` – All API routes

## Author
**Yzabelle Grace Cane**  
Mapua-Malayan Digital College  
MO-IT152 - Integrative Programming and Technologies
