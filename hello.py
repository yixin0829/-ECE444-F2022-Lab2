from distutils.log import debug
from email import message
from xml.dom import ValidationErr
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp, ValidationError

class RegValidator(object):
    '''
    We will create a custom validator class for Flask-WTF with custom error message
    The validator checks if the string contains a substring 'key'
    '''
    def __init__(self, key:str='@') -> None:
        self.regex=f'.*{key}.*'
        self.key = key

    def __call__(self, form, field):
        if not re.match(self.regex, field.data):
            raise ValidationError(f'Please include an \'{self.key}\' in the email address. \'{field.data}\' is missing an \'{self.key}\'.')

class NameForm(FlaskForm):
    utoronto_validator = RegValidator('utoronto')
    email_validator = RegValidator('@')
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[email_validator])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

# ex2.2: dynamic routing
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# activity 4
@app.route('/form', methods=['GET', 'POST'])
def form():
    form = NameForm()
    ut_email_f = 0
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!') # needs to be rendered in html template

        if old_email is not None and old_email !=form.email.data:
            flash('Looks like you have changed your email!')

        if re.match('.*utoronto.*', form.email.data):
            ut_email_f = 1

        session['name'] = form.name.data # better pratice: use user session to store variables
        session['email'] = form.email.data
        return redirect(url_for('form')) # trick: post/redirect/get_pattern
    
    # get updated name and email before rendering
    print(f'{ut_email_f}')
    return render_template('form.html', form=form, name=session.get('name'), email=session.get('email'), ut_email_f=ut_email_f)

if __name__ == '__main__':
    app.run(debug=True)