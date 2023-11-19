from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY']= '696969BRANDON696969'
    
    from .route import Customer
    
    app.register_blueprint(Customer, url_prefix="/")
    
    return app