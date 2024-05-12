from flask import current_app, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db, mail
from app.models import User, Todo
from app.forms import LoginForm, SignupForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from utils.email_utils import send_password_reset_email, send_email_confirmation

def register_user_routes(app):
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignupForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
            try:
                db.session.add(new_user)
                send_email_confirmation(new_user)
                db.session.commit()
                flash('Your account has been created! Please check your email to confirm your email address.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home'))
            except:
                db.session.rollback()
                flash(f'There was an issue creating your account', 'error')
                return render_template('signup.html', form=form)
        return render_template('signup.html', form=form)
    
    @app.route('/confirm-email/<token>')
    def confirm_email(token):
        user = User.verify_confirmation_token(token)
        if not user:
            flash('The confirmation link is invalid or has expired.', 'error')
            return redirect(url_for('home'))
        if user.email_verified:
            flash('Account already confirmed. Please log in.', 'info')
        else:
            user.email_verified = True
            db.session.commit()
            flash('Your email has been confirmed, thank you!', 'success')
            login_user(user)
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Logged in succesfully!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home'))
            flash('Invalid username or password', 'error')
        return render_template("login.html", form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("You have been logget out.", 'success')
        redirect_view = request.args.get('redirect_view', '/')
        return redirect(redirect_view)

    @app.route('/profile')
    @login_required
    def profile():
        today = datetime.today().date()

        expired_tasks = Todo.query.filter_by(user_id=current_user.id, completed=False).filter(Todo.due_date < today).count()
        due_today_tasks = Todo.query.filter_by(user_id=current_user.id, completed=False).filter(Todo.due_date == today).count()
        upcoming_tasks = Todo.query.filter_by(user_id=current_user.id, completed=False).filter(Todo.due_date > today).count()

        return render_template(
            'profile.html', username=current_user.username,
            email=current_user.email, expired_tasks=expired_tasks,
            due_today_tasks=due_today_tasks, upcoming_tasks=upcoming_tasks)
    
    @app.route('/edit-profile', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = EditProfileForm(obj=current_user)
        
        if form.validate_on_submit():
            if current_user.check_password(form.current_password.data):
                current_user.username = form.username.data
                current_user.email = form.email.data
                if form.new_password.data:
                    current_user.password_hash = generate_password_hash(form.new_password.data)
                try:
                    db.session.commit()
                    flash('Profile updated succesfully!', 'success')
                    return redirect(url_for("profile"))
                except:
                    db.session.rollback()
                    flash('There was an issue updating profile', 'error')
                    return render_template('edit_profile.html', form=form)
            else:
                flash('Incorrect password. Plese try again.', 'error')
        return render_template('edit_profile.html', form=form) 
    
    @app.route('/reset_password_request', methods=['GET', 'POST'])
    def reset_password_request():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password', 'info')
            return redirect(url_for('login'))
        return render_template('reset_password_request.html', form=form)
    
    @app.route('/reset_password/<token>', methods=['GET', 'POST'])
    def reset_password(token): 
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        user = User.verify_reset_token(token)
        if not user:
            flash('This is an invalid or expired token', 'error')
            return redirect(url_for('reset_password_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            db.session.commit()
            flash('Your password has been reset', 'success')
            return redirect(url_for('login'))
        return render_template('reset_password.html', form=form, token=token)