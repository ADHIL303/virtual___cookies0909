from flask import Flask, render_template
import threading, requests

app = Flask(__name__, template_folder='templates', static_folder='static')

def auto_request():
    print("Sending auto request...")
    try:
        requests.get("https://npvj6gfx-5500.inc1.devtunnels.ms/")
    except Exception as e:
        print(f"Auto request failed: {e}")
    
    # Repeat every 10 seconds
    threading.Timer(10, auto_request).start()

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
    # Start the auto request loop before Flask starts
    threading.Thread(target=auto_request, daemon=True).start()

    # Now start Flask
    app.run(debug=True, port=5050)
