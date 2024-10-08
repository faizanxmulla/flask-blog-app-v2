# Flask Blog-App V2

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=flat&logo=vuedotjs&logoColor=%234FC08D)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)

A modern, high-performance social media platform built with Flask and Vue.js, featuring real-time updates, asynchronous processing, and intelligent caching.

## 🚀 Features

### Core Functionality
- **Robust Authentication** - Secure JWT-based user authentication system

- **Content Management** 

  - Create, edit, and delete posts with images

  - Rich text support with safe HTML handling

- **Social Networking**
  - Follow/unfollow system

  - Personalized feed based on followed users

  - User search functionality

- **Interaction**
  - Comment on posts

  - User profiles with engagement metrics

### Advanced Features

- **Asynchronous Processing**
  - CSV export of user data

  - Monthly engagement reports (HTML/PDF)

  - Daily activity reminders

- **Performance Optimization**

  - Redis-based caching with intelligent expiry

  - Batch processing for heavy operations


## 🛠 Technology Stack

- **Backend**: Flask (Python 3.7+)

- **Frontend**: Vue.js with CLI
- **Database**: SQLite with SQLAlchemy ORM
- **Caching**: Redis
- **Task Queue**: Celery
- **UI Framework**: Bootstrap
- **Template Engine**: Jinja2 (for emails)


## 📋 Prerequisites

- Python 3.7 or higher

- Node.js 14.x or higher

- Redis server

- MailHog (for local email testing)


## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/faizanxmulla/flask-blog-app-v2.git
   cd flask-blog-app-v2
   ```

2. **Set up the backend**

   ```bash
   cd backend

   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Start required services**
   ```bash
   # Terminal 1
   redis-server
   
   # Terminal 2
   mailhog
   ```

## 🚦 Running the Application

1. **Start the backend services**
   ```bash
   # Terminal 1 - API Server
   cd backend
   python main.py

   # Terminal 2 - Celery Worker
   cd backend
   celery -A main.celery worker -l info

   # Terminal 3 - Celery Beat
   cd backend
   celery -A main.celery beat --max-interval 1 -l info
   ```

2. **Start the frontend development server**
   ```bash
   cd frontend
   npm run serve
   ```

The application will be available at http://localhost:8080



## 🏗 Architecture

### Database Schema

- **User**: Stores user data, authentication info, and social metrics

- **Post**: Contains post content, metadata, and relationships

- **Comment**: Manages user interactions on posts

- **Follow**: Handles user-to-user relationships


### API Design

RESTful architecture with the following main endpoints:

- Authentication: `/api/register`, `/api/login`, `/api/token/refresh`

- Posts: `/api/post`, `/api/post/<post_id>`

- Feed: `/api/feed`

- User: `/api/user`, `/api/profile/<username>`

- Social: `/api/follow/<username>`, `/api/unfollow/<username>`



## 🤝 Contributing

We welcome contributions! Please follow the steps below:

1. Fork the repository

2. Create your feature branch (`git checkout -b feature/newFeature`)

3. Commit your changes (`git commit -m 'Add some newFeature'`)

4. Push to the branch (`git push origin feature/newFeature`)

5. Open a Pull Request



## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 👏 Acknowledgments

- Inspired by modern social media platforms

- Built as part of the Modern Application Development - II course (Course ID: `BSCS2006`)


## ⭐ Support my work

Do ⭐ the repository, if it inspired you, gave you ideas for your own project or helped you in any way !!!
