# Social Media API Project 📱
This Social Media API project is developed using Django and Django REST Framework, enabling users to interact with a social media-like platform. This project provides the backend core for managing users, posts, and follow relationships, along with interactive features such as likes and comments.

## Key Features ✨
The following features have been implemented within this project:

### User Management (CRUD):

New user registration (Sign Up).

### User login and logout.

Management of user profiles (create, read, update, delete) with fields like biography and profile picture.

### Post Management (CRUD):

Create, read, update, and delete posts.

Each post includes content, author, timestamp, and supports optional media (images/videos).

Ensures that users can only update or delete their own posts.

### Follow System:

Creation of follow relationships between users (Follow / Unfollow).

Users are prevented from following themselves.

### Feed of Posts:

An endpoint to display a personalized feed of posts from users the current user follows, ordered by most recent first.

Likes and Comments:

Ability to like and unlike posts.

Ability to comment on posts.

Comments can only be edited or deleted by their author.

Display of the number of likes and comments on each post.

## Technologies Used 🛠️
### Backend:

Django: Python web framework.

Django REST Framework (DRF): For building powerful and flexible APIs.

Pillow: Python imaging library (used for profile pictures and post media).

### Database:

MySQL: Relational database management system.

