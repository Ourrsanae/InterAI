from app import app 

from flask import Flask
from app.home.upload import home_bp

app = Flask(__name__, static_url_path='/static', static_folder='app/static')

app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run(debug = True)