import os

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(32)

from app import rutas

