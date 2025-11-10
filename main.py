from flask import Flask, render_template
import threading
import time
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

# ------------------------------
# Auto-request function using while loop
# ------------------------------
def auto_request():
    url = "https://virtual-cookies0909.onrender.com"  # your own Render URL
    while True:
        try:
            print("Sending auto request to self...")
            requests.get(url, timeout=10)
        except Exception as e:
            print(f"Auto request failed: {e}")
        time.sleep(300)  # 5 minutes

# ------------------------------
# Flask routes
# ------------------------------
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

# ------------------------------
# Start auto-request in a background thread
# ------------------------------
if __name__ == "__main__":
    threading.Thread(target=auto_request, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
