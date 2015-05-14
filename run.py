from app import app
from app.models import init_db
import os

db = os.path.abspath(os.path.dirname(__file__)) + '/questions.db'
if not os.path.isfile(db):
    init_db()

app.run(debug=True)