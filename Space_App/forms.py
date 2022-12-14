from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    name = StringField('(Optional) Name')
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    location = StringField('(Optional) Location')
    password = PasswordField('Password', validators=[Length(min=6)])
    role = SelectField('Role',
                       choices=[(1, 'Spaceport'), (2, 'Launcher'),
                                (3, 'Enthusiast')],
                       coerce=int)


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserEditForm(FlaskForm):
    """Form to edit user"""

    username = StringField('Username', validators=[DataRequired()])
    name = StringField('(Optional) Name')
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    location = StringField('(Optional) Location')
    password = PasswordField('Password', validators=[Length(min=6)])
    role = SelectField('Role',
                       choices=[(1, 'Spaceport'), (2, 'Launcher'),
                                (3, 'Enthusiast')],
                       coerce=int)


class UserDeleteForm(FlaskForm):
    """Form to delete user"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
