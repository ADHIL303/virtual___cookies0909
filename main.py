from flask import Flask, render_template, request,redirect
import smtplib
import threading
import requests


app=Flask(__name__,template_folder='templates',static_folder='static')
def auto_request():
    print("Sending auto request...")
    requests.get("https://npvj6gfx-5500.inc1.devtunnels.ms/")
    
    # Repeat every 10 seconds
    threading.Timer(10, auto_request).start()

@app.before_first_request
def start_auto_request():
    auto_request()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/project')
def project():
    return render_template('project.html')
@app.route('/services')
def services():
    return render_template('services.html')
@app.route('/team')
def team():
    return render_template('team.html')
if __name__ == "__main__":
    app.run(debug=True,port=5050)