from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class FeatureForm(FlaskForm):

    feature_id = IntegerField('id', validators=[DataRequired(), NumberRange(min=1, max=20)])

    feature_name = StringField('name', validators=[DataRequired(), Length(50)])

    feature_size = StringField('size', validators=[DataRequired(), Length(8)])

    formtype = IntegerField('formtype', validators=[DataRequired(), NumberRange(min=1, max=10)])

    user_id = IntegerField('u_id', validators=[DataRequired(), NumberRange(min=1, max=20)])

    submit = SubmitField("Save")
