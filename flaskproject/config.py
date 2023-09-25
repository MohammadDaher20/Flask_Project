import os


class Config:
    SECRET_KEY = "c7698f43333cc30f76ebb4ca14f7de5a"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "os.environ.get('EMAIL_USER')"
    MAIL_PASSWORD = "os.environ.get('EMAIL_PASS')"
