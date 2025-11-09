from flask import Flask, render_template, request,redirect
import smtplib


app=Flask(__name__,template_folder='templates',static_folder='static')


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