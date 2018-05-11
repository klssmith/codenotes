from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 120)])
    content = TextAreaField('Content', validators=[DataRequired()])
