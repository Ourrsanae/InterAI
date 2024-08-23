from flask import Flask
from app.home.upload import home_bp

app = Flask(__name__)
app.register_blueprint(home_bp, url_prefix='/')



#from app.home import home_bp
#app.register_blueprint(home_bp, url_prefix='/home')
