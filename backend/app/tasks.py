import os 
import csv
import datetime 
from datetime import datetime, timedelta

# import pdfkit
from jinja2 import Template
# from weasyprint import HTML 

from celery.schedules import crontab
from flask import current_app, render_template

from app.models import db, User, Post
from app.workers import celery
from app.messages import mail, dailyReminderEmail

# -----------------

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0, 
        sendDailyReminderMail.s(), 
        name='Reminder every 10 seconds.'
    )

    sender.add_periodic_task(
        crontab(minute=0, hour=19, day_of_month='*'),
        sendDailyReminderMail.s(),
        name = 'Daily reminder everyday @7PM via mail.'
    )

    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),
        sendMERMail.s(),
        name = 'Monthly Engagement Report @1st of every month via mail.'
    )


# -----------------

@celery.task
def hello(name):
    print('INSIDE task')
    print("Hello {} !!".format(name))

@celery.task
def add(a, b):
    return a + b


# 1. DAILY reminder TASKS [Daily Reminder Jobs]
# -----------------------

@celery.task
def sendReminderMail(id):
    user = db.session.query(User).filter_by(id=id).first()

    dailyReminderEmail(user.username, user.email)
    return 'Reminder sent successfully via MAIL !!'


@celery.task
def sendDailyReminderMail():
    users = db.session.query(User).all()

    for user in users:
        last_post = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).first()

        if not last_post or last_post.timestamp < datetime.now() - timedelta(days=1):
            sendReminderMail.delay(user.id)

    return 'Daily Reminder sent successfully via MAIL !!'



# 2. MONTHLY mail - tasks [Scheduled Job - Monthly Engagement Report]
# -------------------------

@celery.task
def sendMERMail(id, email):
    user = db.session.query(User).filter_by(id=id).first()
    total_posts_count = len(user.posts)

    message = render_template('MER.html', 
                            name=user.username, 
                            total_posts_count=total_posts_count, 
                            follower_count=user.follower_count,
                            following_count=user.following_count)
    
    today = datetime.today().strftime('%B-%Y')
    subject = f'BLOGLITE-v2 : Monthly Engagement Report for ({today})'

    mail(user.email, subject=subject, message=message, content='html')

    return f'Monthly review email sent to {user.email}'

# sendMERMail(1, 'faizan@gmail.com')


@celery.task
def sendMonthlyMail():
    users = db.session.query(User).all()
    for user in users:
        sendMERMail.delay(user.id, user.email)

    return 'Monthly mail has been sent.'



# 3. EXPORT tasks [User Triggered Async Job - Export as CSV]
# ----------------

@celery.task
def export_csv():
    with current_app.app_context():

        # 1. Generating Profile CSV
        # -----------------------

        profile_fields = ['id', 'username', 'email', 'followers_count', 'following_count']
        users = db.session.query(User).all()

        rows = []
        for user in users:
            row = [user.id, user.username, user.email,  user.follower_count, user.following_count]
            rows.append(row)

        now = datetime.now().strftime("%d-%m-%Y_%H%M")
        profile_filename = f'profile_{now}.csv'

        csv_path = os.path.join('templates/CSV exports/profile', profile_filename)

        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        print('PROFILE FILE SAVED!!')

        with open(csv_path, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            if csvfile.tell() == 0:
                csvwriter.writerow(profile_fields)

            csvwriter.writerows(rows)


        # 2. Generating Posts CSV
        # -----------------------

        post_fields = ['id', 'title', 'caption', 'timestamp', 'last_updated']
        posts = db.session.query(Post).all()

        # create a list of rows for the csv file
        rows = []
        for post in posts:
            row = [post.id, post.title, post.caption, post.timestamp, post.last_updated]
            rows.append(row)

        now = datetime.now().strftime("%d-%m-%Y_%H%M%S")
        post_filename = f'posts_{now}.csv'

        csv_path = os.path.join('templates/CSV exports/posts', post_filename)

        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        print('POST FILE SAVED!!')

        with open(csv_path, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            if csvfile.tell() == 0:
                csvwriter.writerow(post_fields)

            csvwriter.writerows(rows)

    return  {'status': 'success', 'message': 'Post & Profile CSVs - Created Successfully !!', 'csv_path': csv_path}

