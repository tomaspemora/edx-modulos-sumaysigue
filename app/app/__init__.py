from flask import Flask
from datetime import  datetime
import os
app = Flask(__name__)


#app._static_folder = os.path.abspath('static/')
#print(app.root_path)
from app import views
from app import admin_views
from app import jinjax
#from app import jinja2_templates
