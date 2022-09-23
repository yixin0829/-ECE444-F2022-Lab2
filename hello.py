from distutils.log import debug
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
 name = StringField('What is your name?', validators=[DataRequired()])
 submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
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
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!') # needs to be rendered in html template
            session['name'] = form.name.data # better pratice: use user session to store variables
            return redirect(url_for('form')) # trick: post/redirect/get_pattern
    return render_template('form.html', form=form, name=session.get('name'))

if __name__ == '__main__':
    app.run(debug=True)