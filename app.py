from flask import Flask, render_template, request, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, AnyOf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something hard to guess'


class LoginForm(FlaskForm):
    username = StringField('What is your name?', validators=[InputRequired(message="username-data required!")])
    password = PasswordField('What is your password',
                             validators=[InputRequired(message='password-data required!'),
                                         AnyOf(['dev', 'ml'], message='wrong-password!')])


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/form', methods=['GET', 'POST'])
def form():
    login_form = LoginForm()
    form_dict = {
        'login_form': login_form,
    }
    if login_form.validate_on_submit():
        # login_form.username.data = ''
        return f'<h1>The username is {login_form.username.data}, the password is {login_form.password.data}</h1>'
    page_name = 'Login Form'
    return render_template("form.html", form_dict=form_dict, page_name=page_name)


if __name__ == '__main__':
    app.run(debug=True)
