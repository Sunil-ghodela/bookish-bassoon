from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from models import db, User, Listing, Booking, Review
from routes.main import main_bp
from routes.auth import auth_bp
from routes.listings import listings_bp
from routes.bookings import bookings_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rishikesh_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(listings_bp, url_prefix='/listings')
app.register_blueprint(bookings_bp, url_prefix='/bookings')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Create database tables
with app.app_context():
    db.create_all()
    
    # Create admin user if not exists
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            name='Admin',
            email='admin@example.com',
            password='admin123',  # In production, use a secure password
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

# Add this for Render.com deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
