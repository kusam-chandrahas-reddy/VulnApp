from flask import Flask, redirect, render_template, request, url_for
app =Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        return redirect(url_for('dashboard'))
    else:
        return 'Unsupported Method'

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',username="Chandrahas")

@app.errorhandler(404)
def error404(error):
    return render_template('error.html',error='Page Not Found')

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=5500)