from flask import Flask, render_template, request
app =Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('auth.html')
    elif request.method=='POST':
        return render_template('dashboard.html')
    else:
        return 'Unsupported Method'





if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=5500)