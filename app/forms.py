from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, SubmitField, StringField
from wtforms import validators


class SignupForm(Form):
    username = StringField("Name", [validators.required("enter your name")])
    email = StringField("Email", [validators.required("enter your email"), validators.Email("wrong style")])
    password = PasswordField('Password', [validators.required("enter your password")])
    rePassword = PasswordField('rePassword', [validators.required("enter your password again"),
                                              validators.EqualTo(password, "password is different")])
    submit = SubmitField("Sign UP")



class SigninForm(Form):
    email = StringField("Email", [validators.required("enter your email"),
                                  validators.Email("wrong style")])
    password = PasswordField("Password", [validators.required("enter your password")])
    submit = SubmitField("Sign in")


class PostForm(Form):
    title = StringField("Title", [validators.required("title")])
    content =  TextAreaField("content", [validators.required("content")])
    submit = SubmitField("Post")



class CommentForm(Form):
    name = StringField("Name", [validators.required("name")])
    email = StringField("Email", [validators.required("email")])
    comment = TextAreaField("comment", [validators.required("content")])
    submit = SubmitField("Comment")

