from flask import Flask , render_template , request
import os

def create_app(test_config = None):
    app = Flask(__name__)

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'LoginDB'
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)


    try: 
        os.makedirs(app.instance_path)
    except OSError:
        pass
    print(app.instance_path)

    
    # from db import mysql
    # mysql.init_app(app)
    import db
    db.init_app(app)
    
    import views
    app.register_blueprint(views.authenticationBluePrint)

    @app.route('/')
    def base():
       return render_template('auth/base.html')

    return app
