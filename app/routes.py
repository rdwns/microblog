from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():

    users = { 'username' : 'Ridwan'}

    posts = [
        {
            'author': {'username' : 'John'},
            'body': 'Who killed my dog?'
        },
        {
            'author': {'username' : 'Peter'},
            'body': 'We guys are using made up names!?'
        },
        {
            'author':{'username': 'Wanda'},
            'body':'You took everything from me!'
        }
    ]

    return  render_template('index.html', title='Home', user=users, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login requested for user {}, Remember Me= {}'.format(
            form.username.data, form.rememberMe.data))
        return redirect(url_for('index'))

    return render_template('login.html', form=form)
