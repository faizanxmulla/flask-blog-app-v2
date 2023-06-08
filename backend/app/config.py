SECRET_KEY = 'SECRET_KEY'
SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/flaskblog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
SECURITY_PASSWORD_SALT = 'SALT'
SECURITY_PASSWORD_HASH = 'bcrypt'
WTF_CSRF_ENABLED = False
JWT_SECRET_KEY = 'JWT_SECRET_KEY'

UPLOAD_FOLDER = 'static/posts/'
PROFILE_PICS_FOLDER = 'static/profile'

EMAIL_TEMPLATES = 'templates/'
# EXPORT_FOLDER = 'backend/templates/CSV exports/'
# PDF_TEMPLATES = 'backend/templates/'

POSTS_PER_PAGE = 4
ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'png', 'jpeg']
MAX_CONTENT_LENGTH = 8 * 1024 * 1024

CACHE_TYPE = "RedisCache"
CACHE_REDIS_URL = "redis://localhost:6379/0"
CACHE_DEFAULT_TIMEOUT = 300
DEBUG = False

CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"