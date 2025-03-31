from flask import Flask, redirect, render_template, request, url_for, make_response, session
app =Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        username=request.form.get('username')
        if username in ['chandrahas,admin,guest,frontenduser,dev']:
            session['username']=username
        return redirect(url_for('dashboard'))
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


if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=5500)