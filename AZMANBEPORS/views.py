import functools
from flask import (
    Blueprint , flash , g , redirect , render_template , request , session , url_for
)
from werkzeug.security import check_password_hash , generate_password_hash
from db import mysql



authenticationBluePrint = Blueprint('auth' , __name__ , url_prefix='/auth')
gradesBluePrint = Blueprint('grade' , __name__ , url_prefix='/grade')

@authenticationBluePrint.route('/register' , methods=['POST' , 'GET'])
def register():
    cursor = get_cursor()
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        error = None
        if not userName:
            error = 'please enter username'
        elif not password:
            error = 'please enter password'
        else :
            cursor.execute('SELECT ID FROM users WHERE username = %s' ,(userName,))
            a = cursor.fetchone()
            if a is not None:
                error = 'username is taken'
        if error is None:
            cursor.execute('INSERT INTO users (username,password) VALUES(%s,%s)' , (userName,generate_password_hash(password) ,) )
            mysql.connection.commit()
            return redirect(url_for('auth.login'))
        else:
            flash(error)
    return render_template('auth/register.html')

@authenticationBluePrint.route('/mregister' , methods=['POST' , 'GET'])
def mregister():
    b= True
    cursor = get_cursor()
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        error = None
        if not userName:
            error = 'please enter username'
        elif not password:
            error = 'please enter password'
        else :
            cursor.execute('SELECT ID FROM users WHERE username = %s' ,(userName,))
            a = cursor.fetchone()
            if a is not None:
                error = 'username is taken'
        if error is None:
            cursor.execute('INSERT INTO users (username,password) VALUES(%s,%s)' , (userName,generate_password_hash(password) ,) )
            mysql.connection.commit()
            b = False

    returnDict = { "error" : b , "errorMessage" : error , "userName" : userName  }
    return returnDict

@authenticationBluePrint.route('/login' , methods=['POST' , 'GET'])
def login():
    cursor = get_cursor()
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        cursor.execute('SELECT * FROM users WHERE username = %s' , (userName,) )
        user = cursor.fetchone()
        error = None

        if user is None:
            error = 'username not founded'
        elif not check_password_hash(user[2], password):
            error = 'password incorrect'
        if error is None :
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('auth.index'))
        flash(error)

    return render_template('auth/login.html')

@authenticationBluePrint.route('/mlogin' , methods=['POST' , 'GET'])
def mlogin():
    b = True
    cursor = get_cursor()
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        cursor.execute('SELECT * FROM users WHERE username = %s' , (userName,) )
        user = cursor.fetchone()
        error = None

        if user is None:
            error = 'username not founded'
        elif not check_password_hash(user[2], password):
            error = 'password incorrect'
        if error is None :
            b = False

    returnDict = { "error" : b , "errorMessage" : error , "userName" : userName  }
    return returnDict

@authenticationBluePrint.route('/index' , methods=['POST','GET'])
def index():
    cursor = get_cursor()
    user_id = session.get('user_id')
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    return render_template('auth/index.html' , user =  user)

@authenticationBluePrint.before_app_request
def load_logged_in_user():
    cursor = get_cursor()
    user_id = session.get('user_id')
    if user_id is None :
         g.user = None
    else:
        print(cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,)))
        g.user = cursor.fetchone()
        print(g.user)

@authenticationBluePrint.route('/logout' , methods = ['POST' , 'GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.register'))

def get_cursor():
    return mysql.connection.cursor()
    # return mysql.connection.cursor(dict=True)

# @gradesBluePrint.route('/')
# def grades():
    
