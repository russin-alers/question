from flask import Flask

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    DEBUG=True,
    SECRET_KEY='secret key',
)
from app import views, models, forms
