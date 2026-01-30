from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSIONS_FILE = os.path.join(BASE_DIR, 'submissions.json')

# Helper functions for contact form persistence
def _load_submissions():
    try:
        if os.path.exists(SUBMISSIONS_FILE):
            with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def _save_submissions(subs):
    try:
        with open(SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(subs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving submissions: {e}")

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        submission = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        subs = _load_submissions()
        subs.append(submission)
        _save_submissions(subs)
        
        return redirect(url_for('contact', success=1))
    
    success = request.args.get('success')
    return render_template('contact.html', success=success)

@app.route('/admin/submissions', methods=['GET'])
def view_submissions():
    """View saved contact submissions as JSON."""
    subs = _load_submissions()
    return jsonify(subs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
