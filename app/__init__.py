from flask import Flask

# Initialize
app = Flask(__name__, instance_relative_config=True)

__version__ = "0.1"
__notes__ = "released 4 April 2017"
__author__ = "Camilo QS"
__license__ = "GPLv3"

# Set views
from app import views

# Config file
app.config.from_object('config')
