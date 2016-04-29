

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 12:39:22 2016

@author: UltraBook
"""

import os
from flask import Flask, request, redirect, url_for,send_from_directory, render_template
from flask_mail import Mail, Message
from werkzeug import secure_filename

FILENAME = []

UPLOAD_FOLDER = 'downloaded'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
mail = Mail(app)



app.config.update(
	DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = '20x170316@gmail.com',
	MAIL_PASSWORD = 'wssapkcuf',
    UPLOAD_FOLDER = UPLOAD_FOLDER
	)

mail=Mail(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
@app.route('/')
def index():
    
    return render_template('index.html')
    
    
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    password = 'test'
    try:
        if password == request.form['inputPassword']:
           # session['user'] = 'hello'
            return redirect('/userHome')
        else:
            return('Wrong password')
            
    except:
        return ('Wrong password')
           
@app.route('/userHome')
def userhome():
    #if session.get('user'):
    return render_template('chooseFiles.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            NAME, EXT = filename.split('.')
            req = NAME+'/'+EXT
            msg = Message(
                      'From Uploader',
        	       sender='20x170316@gmail.com',
        	       recipients=['x.ssej.x@gmail.com'])
            with app.open_resource(file) as fp:
                msg.attach(filename, req, fp.read())
            mail.send(msg)  
            return redirect('/sent')
 
@app.route('/sent')
def nowwhat():
    return render_template('nowwhat.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
                               
app.run(debug=True)