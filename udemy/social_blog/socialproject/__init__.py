from flask import Flask
from socialproject.core.views import core
from socialproject.error_pages.handlers import error_pages

app = Flask(__name__)

app.register_blueprint(core)
app.register_blueprint(error_pages)