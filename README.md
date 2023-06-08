
# flask-blog-app-v2

A web application where users can register, login, create and manage posts, comment on other users' posts, follow and unfollow other users, and search for other users. Additional features include : Backend jobs like export, alert and reporting jobs.


##
## Features : 

- **User authentication** : Signup and Login (Token Based Authentication - JWT).

- **Account management** : Create, view, edit, and delete user accounts.

- **Content management** : Create, view, edit, and delete posts.

- **User profile** : View own posts, followers, and follows.

- **User feedback** : Comment on posts to express opinions.

- **Explore other users** : View their posts, followers, and follows.

- **Social features** : Search, follow, and unfollow other users.

- **Personalized feed** : View posts from followed users.

- **RESTful API** : API available for posts, users, comments, and follows.

- **User-Triggered Async Jobs** : Download user's posts as a CSV file.

- **Daily Reminder Jobs** : Receive daily reminders to post.

- **Scheduled Jobs** : Receive a report as an email or PDF summarizing engagement for the month.

- **Performance and Caching** - added caching & cache expiry where required to increase the API performance.

##
## Technologies Used : 

- **Flask**: backend API is developed using Flask, a lightweight and flexible web framework for Python.

- **VueJS**: frontend UI is built using VueJS CLI, a popular JavaScript framework for building user interfaces.

- **Jinja2 templates**: used for rendering HTML templates and sending emails.

- **Bootstrap**: used for styling and UI components to create an attractive and responsive user interface.

- **SQLite and SQLAlchemy**: SQLite database is used for data storage, and SQLAlchemy is used as an ORM (Object-Relational Mapping) tool to interact with the database.

- **Flask-Restful**: used to develop the RESTful API for the app

- **Flask-SQLAlchemy**: used to access and modify the app's SQLite database.

- **Flask-Celery**: used for asynchronous background jobs at the backend.

- **Flask-Caching**: used for caching API outputs and increasing performance.

- **Redis**: used as an in-memory database for the API cache and as a message broker for celery.

- **Git**: responsible for version control.


##
## Instructions to run the application.

1. Clone the repo.

2. Navigate to the root folder of the application.

3. Open two separate terminals and execute the following commands in each:

```
redis-server
mailhog
```

4. Navigate to the backend folder and open three separate terminals. Execute the following commands in each:


```
BACKEND : python main.py
WORKERS : celery -A main.celery worker -l info
BEATS : celery -A main.celery beat --max-interval 1 -l info
```

5. Navigate to the frontend folder.

In the terminal, execute the following command:

```
npm run serve
```

These steps will successfully run the application, allowing you to access it from your web browser at http://localhost:8080.

##
## Contributing

Contributions are always welcome !!

If you would like to contribute to the project, please fork the repository and make a pull request.


##
## Support my work 
Do ⭐ the repository, if it inspired you, gave you ideas for your own project or helped you in any way !!!

