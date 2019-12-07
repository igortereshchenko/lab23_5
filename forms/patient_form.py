from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

class PatientForm(FlaskForm):

    patient_id = StringField('id', validators=[DataRequired(), Length(8)])

    patient_age = IntegerField('age', validators=[DataRequired("Please enter your age."), NumberRange(min=18, max=100)])

    patient_height = FloatField('height', validators=[DataRequired(), NumberRange(min=80, max=250)])

    patient_weight = FloatField('weight', validators=[DataRequired(), NumberRange(min=20, max=250)])

    patient_temperature = FloatField('temperature', validators=[DataRequired(), NumberRange(min=34.0, max=43.0)])

    submit = SubmitField("Save")