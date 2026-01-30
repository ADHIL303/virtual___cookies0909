from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='templates', static_folder='static')

# --------------------------------------------------
# File Upload Configuration
# --------------------------------------------------
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --------------------------------------------------
# Database Configuration
# --------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///virtual_cookies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------------------------------------
# Database Models
# --------------------------------------------------
class TeamMember(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    project_link = db.Column(db.String(500), nullable=True)

# --------------------------------------------------
# Mail Configuration (GMAIL)
# --------------------------------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'virtualcookiein@gmail.com'
app.config['MAIL_PASSWORD'] = 'yrjvttoyfeejqgpn'  # ✅ NO SPACES
app.config['MAIL_DEFAULT_SENDER'] = 'virtualcookiein@gmail.com'

mail = Mail(app)

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.route('/')
def index():
    team_members = TeamMember.query.all()
    services = Service.query.all()
    projects = Project.query.all()
    return render_template('index.html' , team=team_members, services=services, projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    all_projects = Project.query.all()
    return render_template('projects.html', projects=all_projects)

@app.route('/services')
def services():
    all_services = Service.query.all()
    return render_template('services.html', services=all_services)

@app.route('/team')
def team():
    all_team = TeamMember.query.all()
    return render_template('team.html', team_members=all_team)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        success = request.args.get('success')
        return render_template('contact.html', success=success)

    # ------------------ POST ------------------
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    # Validation
    if not name or not email or not message:
        error = "All fields are required."
        return render_template('contact.html', error=error)

    email_subject = subject if subject else "New Contact Message"

    email_body = f"""
New Contact Form Message

Name    : {name}
Email   : {email}

Message:
{message}
"""

    # ✅ IMPORTANT: recipients added
    msg = Message(
        subject=email_subject,
        recipients=['virtualcookiein@gmail.com'],  # where mail is sent
        body=email_body
    )

    try:
        mail.send(msg)
    except Exception as e:
        print("MAIL ERROR:", e)  # 🔥 see real error in terminal
        error = "Unable to send message right now."
        return render_template('contact.html', error=error)

    return redirect(url_for('contact', success=1))


# --------------------------------------------------
# Admin Routes
# --------------------------------------------------
@app.route('/admin')
def admin():
    all_team = TeamMember.query.all()
    all_services = Service.query.all()
    all_projects = Project.query.all()
    return render_template('admin.html', team_members=all_team, services=all_services, projects=all_projects)

@app.route('/init-db')
def init_db():
    db.create_all()
    return "Database created"
@app.route('/admin/add-team', methods=['POST'])
def add_team_member():
    name = request.form.get('name', '').strip()
    position = request.form.get('position', '').strip()
    image_file = request.files.get('image')

    if not name or not position:
        return redirect(url_for('admin'))

    # Handle image upload
    image_path = "/static/assets/images/pages/shape/cookieshape1.png"  # default image
    
    if image_file and image_file.filename and allowed_file(image_file.filename):
        try:
            filename = secure_filename(image_file.filename)
            import time
            filename = f"{int(time.time())}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image_file.save(filepath)
            image_path = f"uploads/{filename}"
        except Exception as e:
            print(f"Upload error: {e}")
            image_path = "/static/assets/images/pages/shape/cookieshape1.png"

    new_member = TeamMember(name=name, position=position, image=image_path)
    db.session.add(new_member)
    db.session.commit()

    return redirect(url_for('admin'))


@app.route('/admin/add-service', methods=['POST'])
def add_service():
    title = request.form.get('title', '').strip()
    subtitle = request.form.get('subtitle', '').strip()
    description = request.form.get('description', '').strip()
    image_file = request.files.get('image')

    if not title or not subtitle or not description:
        return redirect(url_for('admin'))

    # Handle image upload
    image_path = "/static/assets/images/pages/shape/cookieshape1.png"  # default image
    
    if image_file and image_file.filename and allowed_file(image_file.filename):
        try:
            filename = secure_filename(image_file.filename)
            import time
            filename = f"{int(time.time())}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image_file.save(filepath)
            image_path = f"uploads/{filename}"
        except Exception as e:
            print(f"Upload error: {e}")
            image_path = "/static/assets/images/pages/shape/cookieshape1.png"

    new_service = Service(title=title, subtitle=subtitle, description=description, image=image_path)
    db.session.add(new_service)
    db.session.commit()

    return redirect(url_for('admin'))


@app.route('/admin/delete-team/<int:id>')
def delete_team_member(id):
    member = TeamMember.query.get(id)
    if member:
        db.session.delete(member)
        db.session.commit()
    return redirect(url_for('admin'))


@app.route('/admin/delete-service/<int:id>')
def delete_service(id):
    service = Service.query.get(id)
    if service:
        db.session.delete(service)
        db.session.commit()
    return redirect(url_for('admin'))


@app.route('/admin/add-project', methods=['POST'])
def add_project():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    client = request.form.get('client', '').strip()
    category = request.form.get('category', '').strip()
    start_date = request.form.get('start_date', '').strip()
    end_date = request.form.get('end_date', '').strip()
    project_link = request.form.get('project_link', '').strip()
    image_file = request.files.get('image')

    if not title or not description or not client or not category or not start_date or not end_date:
        return redirect(url_for('admin'))

    # Handle image upload
    image_path = "/static/assets/images/pages/shape/cookieshape1.png"  # default image
    
    if image_file and image_file.filename and allowed_file(image_file.filename):
        try:
            filename = secure_filename(image_file.filename)
            import time
            filename = f"{int(time.time())}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image_file.save(filepath)
            image_path = f"uploads/{filename}"
        except Exception as e:
            print(f"Upload error: {e}")
            image_path = "/static/assets/images/pages/shape/cookieshape1.png"

    new_project = Project(title=title, description=description, client=client, category=category, 
                         start_date=start_date, end_date=end_date, image=image_path, project_link=project_link if project_link else None)
    db.session.add(new_project)
    db.session.commit()

    return redirect(url_for('admin'))


@app.route('/admin/delete-project/<int:id>')
def delete_project(id):
    project = Project.query.get(id)
    if project:
        db.session.delete(project)
        db.session.commit()
    return redirect(url_for('admin'))


# --------------------------------------------------
# Run App
# --------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)