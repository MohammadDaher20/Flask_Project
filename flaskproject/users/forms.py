from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user

from flaskproject.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])

    # to confirm pass we should compare the first and second pass so we need the equalto validator
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=8), EqualTo("password")],
    )
    submit = SubmitField("Sign Up")

    # >>>>   limitation of username ( unique, didn't exist)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose another one")

    # >>>>  limitation of email ( unique, didn't exist)
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose another one")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])

    picture = FileField(
        "Update profile picture", validators=[FileAllowed(["jpg", "jpeg", "png"])]
    )

    submit = SubmitField("Update")

    # >>>>   limitation of username ( unique, didn't exist)
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            # we can't update the username/email into others username and email
            if user:
                raise ValidationError(
                    "That username is taken. Please choose another one"
                )

    # >>>>  limitation of email ( unique, didn't exist)
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            # we can't update the username/email into others username and email
            if user:
                raise ValidationError("That email is taken. Please choose another one")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    # >>>>  if the email doesn't exist
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with this email! You must register first."
            )


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])

    # to confirm pass we should compare the first and second pass so we need the equalto validator
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=8), EqualTo("password")],
    )
    submit = SubmitField("Reset Password")
