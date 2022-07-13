from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, AnyOf
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class LoginForm(FlaskForm):
    username = StringField('What is your name?', validators=[InputRequired(message="username-data required!")])
    password = PasswordField('What is your password',
                             validators=[InputRequired(message='password-data required!'),
                                         AnyOf(['dev', 'ml'], message='wrong-password!')])


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship('user', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.id


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.id'),
                     nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


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
        session['name'] = login_form.username.data
        return f'<h1>The username is {login_form.username.data}, the password is {login_form.password.data}</h1>'
    page_name = 'Login Form'
    return render_template("form.html", form_dict=form_dict, page_name=page_name)


if __name__ == '__main__':
    app.run(debug=True)
