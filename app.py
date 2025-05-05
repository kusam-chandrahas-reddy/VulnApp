from flask import Flask, redirect, render_template, request, url_for, make_response, session
app =Flask(__name__)
app.secret_key=b'mypowerfulsecretkey'


#########################

import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('db_schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#list of users
def lusers(cols='*'):
    db = get_db()
    cur = db.execute('SELECT {} FROM users'.format(cols))
    users = cur.fetchall()
    return users

######################################################


userslist = ['chandrahas','admin','guest','frontenduser','dev']

@app.route('/')
def index():
    listusers=lusers()
    return render_template('index.html',listusers='Users: ' + str(listusers))

@app.route('/auth', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        
        print('Username:',username)
        
        listusers=lusers('username,password')
        usersdict=dict(listusers)
        usernames=[x[0] for x in listusers]
        passwords=[x[1] for x in listusers]
        if username in usernames:
            if password == usersdict[username]:
                session['username']=username
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html',message="Password is incorrect")
        else:
            return render_template('login.html',message="Username is incorrect")
    else:
        return 'Unsupported Method'

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html',username=session.get('username'))
    else:
        return redirect(url_for('login'))
    
@app.errorhandler(404)
def error404(error):
    resp=make_response(render_template('error.html',error='Page Not Found'))
    resp.headers['error-status']=404
    return resp

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method=='GET':
        return render_template('register.html')
    elif request.method=='POST':
        username=request.form['username']
        print('Username:',username)
        if username not in userslist:
            userslist.append(username)
            session['username']=username
            return redirect(url_for('dashboard'))
        else:
            return render_template('register.html',message="Error occurred in Registration, Please Try Again")
    else:
        return 'Unsupported Method'


if __name__=='__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=5500)