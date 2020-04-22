from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ForgotPasswordForm, PasswordResetForm
from app.models import User
from app.auth.email import send_password_reset_mail



@bp.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title=_('Register'), form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid Username or Password!'))
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.rememberMe.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page=url_for('main.index')

        return redirect(next_page)

    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_mail(user)
        flash(_('Please check your email for instructions to reset your password!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/forgotpassword.html', title = _("Forgot Password"), form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_token(token)

    if not user:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)












