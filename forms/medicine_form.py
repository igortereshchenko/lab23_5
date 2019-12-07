from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

class MedicineForm(FlaskForm):


    medicine_name = StringField('name', validators=[DataRequired(), Length(10)])

    price = FloatField('price', validators=[DataRequired(), NumberRange(min=0, max=1000)])

    vendor = StringField('vendor', validators=[DataRequired(), Length(8)])

    city = StringField('city', validators=[DataRequired(), Length(8)])


    submit = SubmitField("Save")