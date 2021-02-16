from config import config
from flask import Flask, render_template

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint)

	return app
