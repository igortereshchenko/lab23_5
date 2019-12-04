from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length, AnyOf

class CarForm(FlaskForm):

    number = IntegerField('number', validators=[DataRequired()])

    model = StringField('model', validators=[DataRequired(), AnyOf('m1','m2')])

    color = StringField('color', validators=[DataRequired()])

    price = IntegerField('price', validators=[DataRequired(), NumberRange(min = 0)])

    user_id = IntegerField('id', validators=[DataRequired(), NumberRange(min=1, max=20)])

    submit = SubmitField("Save")

