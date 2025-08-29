# 📱 Social Media API Project

This Social Media API project is developed using **Django** and **Django REST Framework**, enabling users to interact with a social media-like platform.  
It provides the backend core for managing **users, posts, and follow relationships**, along with interactive features such as **likes** and **comments**.

---

## ✨ Key Features

### 👤 User Management (CRUD)
- New user registration (**Sign Up**).  
- User login and logout.  
- Management of user profiles (**create, read, update, delete**) with fields like biography and profile picture.  

### 📝 Post Management (CRUD)
- Create, read, update, and delete posts.  
- Each post includes content, author, timestamp, and supports optional media (images/videos).  
- Ensures that users can only update or delete **their own posts**.  

### 🤝 Follow System
- Creation of follow relationships between users (**Follow / Unfollow**).  
- Users are prevented from following themselves.  

### 📰 Feed of Posts
- Endpoint to display a **personalized feed** of posts from users the current user follows.  
- Posts are ordered by most recent first.  

### ❤️ Likes and 💬 Comments
- Ability to **like** and **unlike** posts.  
- Ability to **comment** on posts.  
- Comments can only be **edited or deleted** by their author.  
- Display of the **number of likes and comments** on each post.  

---

## 🛠️ Technologies Used

### 🔙 Backend
- **Django**: Python web framework.  
- **Django REST Framework (DRF)**: For building powerful and flexible APIs.  
- **Pillow**: Python imaging library (used for profile pictures and post media).  

### 🗄️ Database
- **MySQL**: Relational database management system.  

---

## 📌 API Endpoints

### 👤 User Endpoints
1. **Register User**  
   - **POST** `/api/users/register/`  
   **Request Body:**
   ```json
   {
     "username": "JohnDoe",
     "email": "john@example.com",
     "password": "SecurePass123!"
   }

Response:

```json
{
  "message": "User registered successfully"
}
Login User

POST /api/users/login/
Request Body:

```json
{
  "username": "JohnDoe",
  "password": "SecurePass123!"
}
Response:

```json
{
  "token": "your-jwt-token"
}
User Profile (CRUD)

GET /api/users/{id}/

PUT /api/users/{id}/

DELETE /api/users/{id}/

📝 Post Endpoints
Create Post

POST /api/posts/
Request Body:

```json
{
  "content": "Hello World!",
  "media": "optional_image_or_video.jpg"
}
Get All Posts

GET /api/posts/

Update/Delete Post (owner only)

PUT /api/posts/{id}/

DELETE /api/posts/{id}/

Like/Unlike Post

POST /api/posts/{id}/like/

POST /api/posts/{id}/unlike/

Comment on Post

POST /api/posts/{id}/comments/

PUT /api/comments/{id}/

DELETE /api/comments/{id}/

🤝 Follow Endpoints
Follow User

POST /api/follows/{id}/

Unfollow User

DELETE /api/follows/{id}/

Get Followers & Following

GET /api/follows/followers/{id}/

GET /api/follows/following/{id}/

🔔 Notification Endpoints
Get Notifications

GET /api/notifications/

Mark Notification as Read

PUT /api/notifications/{id}/read/

🚀 How to Run Locally
Clone the repository:

$bash

git clone <repo-link>
cd social_media_api
Create and activate a virtual environment:

$bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
Install dependencies:

$bash
pip install -r requirements.txt
Run migrations:

$bash
python manage.py migrate
Start the development server:

$bash
python manage.py runserver
Access the API at:

cpp
http://127.0.0.1:8000/
