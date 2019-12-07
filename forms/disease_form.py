from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class DiseaseForm(FlaskForm):
    disease_id = StringField('id', validators=[DataRequired(), Length(8)])
    disease_name = StringField('name', validators=[DataRequired(), Length(20)])
    severity = IntegerField('severity', validators=[DataRequired(), NumberRange(min=1, max=10)])
    symptom_id = StringField('symptom_id', validators=[DataRequired(), Length(8)])

    submit = SubmitField("Save")
