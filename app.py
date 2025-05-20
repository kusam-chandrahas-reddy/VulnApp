from flask import Flask, redirect, render_template, request, url_for, make_response, session
from flask_cors import CORS, cross_origin

app =Flask(__name__)
app.secret_key=b'mypowerfulsecretkey'

#cors = CORS(app, resources={ r"/changepwd": {"origins": "http://localhost:5500"}}, supports_credentials=True)

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
def lusers(cols='*',where=None):
    db = get_db()
    if where is None:
        cur = db.execute('SELECT {} FROM users'.format(cols))
    else:
        q='SELECT {} FROM USERS WHERE {};'.format(cols,where)
        print(q)
        cur=db.execute(q)
        
    users = cur.fetchall()
    return users

def runquery(query,data):
    db = get_db()
    cur=db.cursor()
    cur.execute(query,data)
    db.commit()
    return cur.rowcount
    #users = cur.fetchall()
    #return users

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


@app.route('/myprofile', methods=['GET','POST'])
def myprofile():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method=='GET':
        profile=('username','email','full_name')
        print('username='+str(session.get('username')))
        listusers=lusers('username,email,fullname','username=\''+str(session.get('username'))+'\'')
        profile=dict(zip(profile,listusers[0]))
        print(profile)
        return render_template('profile.html',profile=profile)
    elif request.method=='POST':
        return render_template('profile.html')
    else:
        return render_template('profile.html')

@app.route('/changepwd', methods=['GET','POST'])
def password():
    if 'username' in session:
        if request.method=='GET':
            if 'new_password' in session: del session['new_password']
            response = make_response(render_template('changepwd.html',username=session.get('username')))
           # response.headers['Access-Control-Allow-Origin']= 'http://192.168.29.8:5500'
           # response.headers['Access-Control-Allow-Credentials']= 'true'
           # response.headers['Access-Control-Allow-Methods']='POST'
            return response
        elif request.method=='POST':
            user=session.get('username')
            if 'new_password' in request.form and 'confirm_password' in request.form and 'confirmchange' not in request.form:
                np=request.form['new_password']
                cp=request.form['confirm_password']
                if cp != np:
                    return render_template('changepwd.html',username=session.get('username'),message='Entered passwords are mismatching')
                session['new_password']=np
                return render_template('confirmchangepwd.html',username=session.get('username'))
            elif 'new_password' not in request.form and 'confirm_password' not in request.form and 'confirmchange' in request.form and 'new_password' in session:
                confirm=request.form['confirmchange']
                if confirm=='Yes':
                    query='UPDATE users SET password = ? WHERE username= ? ;'
                    data=(session.get('new_password'),session.get('username'))
                    out=runquery(query,data)
                    if out==1:
                        return render_template('changepwd.html',username=session.get('username'),message='Password updated Successfully!!!')
                    else:
                        return render_template('changepwd.html',username=session.get('username'),message='Error occurred while updating password, please try later.')
                    
                elif confirm=='No':
                    return render_template('changepwd.html',username=session.get('username'),message='Password is Not Updated')
                else:
                    return render_template('changepwd.html',username=session.get('username'),message='Invalid Request is sent. Please try again!!!')
            else:
                return render_template('changepwd.html',username=session.get('username'),message='Invalid Request is sent. Please try again!!!')
                
    else:
        return redirect(url_for('login'))


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
        password=request.form['password']
        fullname=request.form['fullname']
        email=request.form['email']
        print('Username:',username)
        usernames=[x[0] for x in lusers('username')]
        if username not in usernames:
            #userslist.append(username)
            query="INSERT OR IGNORE INTO users (username, email, password, fullname) VALUES (?,?,?,?)"
            data=(username,email,password,fullname)
            out=runquery(query,data)
            if out==1:
                message='Registered Successfully'
                session['username']=username
                return redirect(url_for('dashboard'))
            else: return render_template('register.html',message='Registration Failed, Please Try Again')
            
        else:   return render_template('register.html',message="Error occurred in Registration, Please Try Again")
    else:   return 'Unsupported Method'


if __name__=='__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=5500)