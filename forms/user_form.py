from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

class UserForm(FlaskForm):

    user_id = IntegerField('id', validators=[DataRequired(), NumberRange(min=1, max=20)])

    user_name = StringField('name', validators=[DataRequired(), Length(20)])

    user_age = IntegerField('age', validators=[DataRequired(), NumberRange(min=18, max=100)])

    skin_condition = IntegerField('skin', validators=[DataRequired(), NumberRange(min=1, max=10)])

    submit = SubmitField("Save")