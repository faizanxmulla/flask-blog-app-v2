from celery import Celery
from flask import current_app as app

celery = Celery("Application Jobs", 
                broker='redis://localhost:6379/1', 
                backend='redis://localhost:6379/2', 
                imports=["app.tasks"])


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
