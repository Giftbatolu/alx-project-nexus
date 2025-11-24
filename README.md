# MedLoveScience Social Media Feed (Backend Service)
The MedLabScience Social Media Feed is a real-time backend system designed to support a modern, science-focused social networking platform for Medical Laboratory Science students, scientists, and lecturers.

This service enables users to create and manage posts, interact through comments, likes, and reposts, and stay connected through instant, real-time updates tailored to the scientific and academic community.
* Built to facilitate meaningful engagement, the platform allows users to:
* Share insights and discoveries
* Discuss laboratory procedures and best practices
* Follow peers, mentors, and professionals
* Participate in academic and professional conversations

This backend provides the core infrastructure needed to power a reliable, scalable, and interactive social media experience for the MedLabScience community.

## Features
* **User System:** The platform provides a secure and reliable user system that supports account registration and authentication, profile management, and the ability for users to follow or unfollow others within the Medical Laboratory Science community.
* **Posts:** Users can create, edit, and delete posts, share scientific insights or laboratory experiences, attach media, and receive real-time updates as new content becomes available.
* **Interactions:** The system enables users to engage meaningfully with content by commenting on posts, liking or unliking them, reposting information to their own feed, and saving or bookmarking posts for future reference
* **Notifications System:** A robust notification system delivers real-time alerts for likes, comments, reposts, new followers, mentions, and other key activities, ensuring users stay connected and informed at all times.

## Prerequisites
* Python 3.8+
* PostgreSQL
* Git

## Technologies Stack
* Django
* GraphQL
* Token-based Authentication
* PostgreSQL
* Swagger (via drf-yasg)

## Database Schema (ERD)
![alt text](social_feed.drawio.png)
### Entities
* **User:** Represents individuals using the platform, including students, scientists, and lecturers. A user can create posts, follow other users, and engage with content through comments, likes, and reposts.
* **Post:** A post contains the main content shared by users. Each post is created by a user and may include text, media attachments, and interaction data such as likes, comments, and reposts.
* **Comment:** Comments allow users to respond to posts or engage in discussions. Each comment is linked to both a specific post and the user who created it.
* **Like:** A like represents a user’s positive interaction with a post. It connects a user to a post and can be added or removed at any time.
* **Report:** (Repost/Share) enables users to reshare another user’s post onto their own feed. It links the reposting user to the original post.
* **Follow:** The follow relationship connects one user to another, enabling followers to see updates or posts from users they are interested in.
* **Post_media:** Represents media files (images, videos, documents) attached to posts. Each media entry is associated with a specific post and stored with relevant metadata.

### Entity Relationships
* **User — Post (1:Many):** A user can create many posts, but each post belongs to one user.
* **User — Comment (1:Many):** A user can write many comments, and each comment is authored by a single user.
* **Post — Comment (1:Many):** A post can have many comments, but each comment is linked to one specific post.
* **User — Like (1:Many):** A user can like many posts, and each like action is performed by one user.
* **Post — Like (1:Many):** A post can receive many likes, each tied to a user who performed the action.
* **User — Follow (1:Many self-relationship):** Users can follow multiple other users, and this is a self-referential relationship where One user (follower) follows another user (followed).
* **User — Repost (1:Many):** A user can repost multiple posts, and each repost is associated with exactly one user.
* **Post — Repost (1:Many):** A post can be reposted many times, with each repost linked back to the original post.
* **Post — Post_Media (1:N):** A single post can contain multiple media files, but each media file belongs to one post.