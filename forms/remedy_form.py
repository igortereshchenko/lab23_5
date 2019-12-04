from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class RemedyForm(FlaskForm):

    remedy_id = IntegerField('id', validators=[DataRequired(), NumberRange(min=1, max=20)])

    remedy_name = StringField('name', validators=[DataRequired(), Length(20)])

    remedy_color = StringField('color', validators=[DataRequired(), Length(20)])

    remedy_brightness = StringField('brightness', validators=[DataRequired(), Length(10)])

    feature_id = IntegerField('f_id', validators=[DataRequired(), NumberRange(min=1, max=20)])

    submit = SubmitField("Save")
