from flask import Flask, render_template, request, redirect
from forms.patient_form import PatientForm
from forms.symptom_form import SymptomForm
from forms.disease_form import DiseaseForm
from forms.medicine_form import MedicineForm
import uuid
import json
import plotly
from sqlalchemy.sql import func
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:goloborodko77@localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://edthclqwflfvhn:025c9772d54701192e421df511b59b84d0abb0d4d98ef8cf57dbd7e6ce9c9d26@ec2-174-129-255-21.compute-1.amazonaws.com:5432/dfs5vsme1mbn3q'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class SymptomHasMedicine(db.Model):
    __tablename__ = 'symptom_has_medicine'

    symptom_id = db.Column(db.String(8), db.ForeignKey('orm_symptom.symptom_id'), primary_key=True)
    medicine_name = db.Column(db.String(10), db.ForeignKey('orm_medicine.medicine_name'), primary_key=True)

    symptom = db.relationship('OrmSymptom', back_populates="medicine")
    medicine = db.relationship('OrmMedicine', back_populates="symptom")

class OrmPatient(db.Model):
    __tablename__ = 'orm_patient'

    patient_id = db.Column(db.String(8), primary_key=True)
    patient_age = db.Column(db.Integer, nullable=False)
    patient_height = db.Column(db.Float, nullable=False)
    patient_weight = db.Column(db.Float, nullable=False)
    patient_temperature = db.Column(db.Float, nullable=False)

    symptom = db.relationship('OrmSymptom')


class OrmSymptom(db.Model):
    __tablename__ = 'orm_symptom'

    symptom_id = db.Column(db.String(8), primary_key=True)
    description = db.Column(db.String(50), nullable=False)

    patient_id = db.Column(db.String(8), db.ForeignKey('orm_patient.patient_id'))

    disease = db.relationship('OrmDisease')

    medicine = db.relationship('SymptomHasMedicine')

class OrmDisease(db.Model):
    __tablename__ = 'orm_disease'

    disease_id = db.Column(db.String(8), primary_key=True)
    disease_name = db.Column(db.String(20), nullable=False)
    severity = db.Column(db.Integer, nullable=False)

    symptom_id = db.Column(db.String(8), db.ForeignKey('orm_symptom.symptom_id'))

#--------------------
# class OrmRecommendation(db.Model):
#     __tablename__ = 'orm_recommendation'
#
#     recommendation_id = db.Column(db.String(8), primary_key=True)
#     recommendation_name = db.Column(db.String(20), nullable=False)
#     disease_id = db.Column(db.String(8), db.ForeignKey('orm_disease.disease_id'))

class OrmMedicine(db.Model):
    __tablename__ = 'orm_medicine'

    medicine_name = db.Column(db.String(10), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    vendor = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)

    symptom = db.relationship('SymptomHasMedicine')

# db.session.query(SymptomHasMedicine).delete()
# db.session.query(OrmMedicine).delete()
# db.session.query(OrmDisease).delete()
# db.session.query(OrmSymptom).delete()
# db.session.query(OrmPatient).delete()
db.drop_all()
db.create_all()

Nastya = OrmPatient(
    patient_id='Nastya',
    patient_age=19,
    patient_height=190,
    patient_weight=77,
    patient_temperature=37.7
)

Max = OrmPatient(
    patient_id='Max',
    patient_age=20,
    patient_height=166,
    patient_weight=56,
    patient_temperature=36.9
)

Serg = OrmPatient(
    patient_id='Serg',
    patient_age=29,
    patient_height=196,
    patient_weight=49,
    patient_temperature=37.1
)

Kate = OrmPatient(
    patient_id='Kate',
    patient_age=43,
    patient_height=163,
    patient_weight=77,
    patient_temperature=37.4
)

cough = OrmSymptom(
    symptom_id = '21122253',
    description = 'cough',
    patient_id='Max'
)

throat = OrmSymptom(
    symptom_id = '31122253',
    description = 'throat pain',
    patient_id='Max'
)

head = OrmSymptom(
    symptom_id = '11122253',
    description = 'head pain',
    patient_id='Serg'
)

URTI = OrmDisease(
    disease_id='J00-06',
    disease_name='URTI',
    severity=3,
    symptom_id = '11122253'
)

Flu = OrmDisease(
    disease_id='J10',
    disease_name='Flu',
    severity=4,
    symptom_id = '31122253'
)

Migraine = OrmDisease(
    disease_id='G43.0',
    disease_name='Migraine',
    severity=5,
    symptom_id = '21122253'
)

Cold = OrmDisease(
    disease_id='J00',
    disease_name='Cold',
    severity=3,
    symptom_id = '21122253'
)


db.session.add_all([

    Nastya,
    Max,
    Serg,
    Kate,
    URTI,
    Flu,
    Migraine,
    Cold,
    cough,
    throat,
    head
])

db.session.commit()


@app.route('/')
def root():
    return render_template('index.html')

#---------------------------

@app.route('/get', methods=['GET'])
def create_medicine():
    med1 = OrmMedicine(
        medicine_name='med1',
        price=99,
        vendor='vend1',
        city = 'city1'
    )

    med2 = OrmMedicine(
        medicine_name='med2',
        price=199,
        vendor='vend2',
        city='city2'
    )
    med3 = OrmMedicine(
        medicine_name='med3',
        price=69,
        vendor='vend3',
        city='city3'
    )

    db.session.add_all([med1, med2, med3])
    db.session.commit()
    return render_template('success.html')

@app.route('/show')
def medicines():
    res = db.session.query(OrmMedicine).all()

    return render_template('medicine_table.html', medicines=res)

@app.route('/update/<string:id>', methods=['GET', 'POST'])
def edit_medicine(id):
    form = MedicineForm()
    result = db.session.query(OrmMedicine).filter(OrmMedicine.medicine_name == id).one()

    if request.method == 'GET':

        form.medicine_name.data = result.medicine_name
        form.price.data = result.price
        form.vendor.data = result.vendor
        form.city.data = result.city

        return render_template('edite_medicine.html', form=form, form_name='edit medicine')
    elif request.method == 'POST':

        result.price = form.price.data
        result.vendor = form.vendor.data
        result.city = form.city.data

        db.session.commit()
        return redirect('/show')

# @app.route('/get')
# def recommendations():
#     res = db.session.query(OrmRecommendation).all()
#
#     return render_template('medicine_table.html', recommendations=res)
#
# @app.route('/insert_recommendation', methods=['POST', 'GET'])
# def insert_recommendation():
#     form = RecommendationForm()
#
#     if request.method == 'POST':
#         new_recommendation = OrmRecommendation(
#             recommendation_id=form.recommendation_id.data,
#             recommendation_name=form.recommendation_name.data,
#             disease_id=form.disease_id.data
#         )
#         db.session.add(new_recommendation)
#         db.session.commit()
#         return render_template('success.html')
#     elif request.method == 'GET':
#         return render_template('recommendation_form.html', form=form)
#-----------------------------------------------

@app.route('/patients')
def patients():
    res = db.session.query(OrmPatient).all()

    return render_template('patients_table.html', patients=res)

@app.route('/create_patient', methods=['POST', 'GET'])
def create_patient():
    form = PatientForm()

    if request.method == 'POST':
        new_patient = OrmPatient(
            patient_id=form.patient_id.data,
            patient_age=form.patient_age.data,
            patient_height=form.patient_height.data,
            patient_weight=form.patient_weight.data,
            patient_temperature=form.patient_temperature.data
        )
        db.session.add(new_patient)
        db.session.commit()
        return render_template('success.html')
    elif request.method == 'GET':
        return render_template('patient_form.html', form=form)


@app.route('/patient_edit/<string:id>', methods=['GET', 'POST'])
def edit_patient(id):
    form = PatientForm()
    result = db.session.query(OrmPatient).filter(OrmPatient.patient_id == id).one()

    if request.method == 'GET':

        form.patient_id.data = result.patient_id
        form.patient_age.data = result.patient_age
        form.patient_height.data = result.patient_height
        form.patient_weight.data = result.patient_weight
        form.patient_temperature.data = result.patient_temperature

        return render_template('edit_patient.html', form=form, form_name='edit patient')
    elif request.method == 'POST':

        result.patient_age = form.patient_age.data
        result.patient_height = form.patient_height.data
        result.patient_weight = form.patient_weight.data
        result.patient_temperature = form.patient_temperature.data

        db.session.commit()
        return redirect('/patients')

@app.route('/delete_patient/<string:id>', methods=['GET', 'POST'])
def delete_patient(id):
    result = db.session.query(OrmPatient).filter(OrmPatient.patient_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')

# SYMPTOM
@app.route('/symptoms')
def symptoms():
    res = db.session.query(OrmSymptom).all()

    return render_template('symptoms_table.html', symptoms=res)

@app.route('/new_symptom', methods=['GET', 'POST'])
def new_symptom():
    form = SymptomForm()

    if request.method == 'POST':
        new_symptom = OrmSymptom(
            symptom_id=form.symptom_id.data,
            description=form.description.data,
            patient_id=form.patient_id.data
        )
        db.session.add(new_symptom)
        db.session.commit()
        return render_template('success.html')
    elif request.method == 'GET':
        return render_template('symptom_form.html', form=form)

@app.route('/edit_symptom/<string:id>', methods=['GET', 'POST'])
def edit_symptom(id):
    form = SymptomForm()
    result = db.session.query(OrmSymptom).filter(OrmSymptom.symptom_id == id).one()

    if request.method == 'GET':

        form.symptom_id.data = result.symptom_id
        form.description.data = result.description
        form.patient_id.data = result.patient_id

        return render_template('edit_symptom.html', form=form, form_name='edit symptom')
    elif request.method == 'POST':

        result.description = form.description.data
        result.patient_id = form.patient_id.data

        db.session.commit()
        return redirect('/symptoms')


@app.route('/delete_symptom/<string:id>', methods=['GET', 'POST'])
def delete_symptom(id):
    result = db.session.query(OrmSymptom).filter(OrmSymptom.symptom_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')


# DISEASE
@app.route('/diseases')
def diseases():
    res = db.session.query(OrmDisease).all()

    return render_template('diseases_table.html', diseases=res)


@app.route('/new_disease', methods=['GET', 'POST'])
def new_disease():
    form = DiseaseForm()

    if request.method == 'POST':
        new_disease = OrmDisease(
            disease_id=form.disease_id.data,
            disease_name=form.disease_name.data,
            severity=form.severity.data,
            symptom_id=form.symptom_id.data

        )
        db.session.add(new_disease)
        db.session.commit()
        return render_template('success.html')
    elif request.method == 'GET':
        return render_template('disease_form.html', form=form)


@app.route('/edit_disease/<string:id>', methods=['GET', 'POST'])
def edit_disease(id):
    form = DiseaseForm()
    result = db.session.query(OrmDisease).filter(OrmDisease.disease_id == id).one()

    if request.method == 'GET':

        form.disease_id.data = result.disease_id
        form.disease_name.data = result.disease_name
        form.severity.data = result.severity
        form.symptom_id.data = result.symptom_id

        return render_template('edit_disease.html', form=form, form_name='edit disease')
    elif request.method == 'POST':

        result.disease_name = form.disease_name.data
        result.severity = form.severity.data
        result.symptom_id = form.symptom_id.data

        db.session.commit()
        return redirect('/diseases')


@app.route('/delete_disease/<string:id>', methods=['GET', 'POST'])
def delete_disease(id):
    result = db.session.query(OrmDisease).filter(OrmDisease.disease_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')

@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    my_query = (
        db.session.query(
            OrmPatient.patient_id,
            func.count(OrmSymptom.symptom_id).label('symptom_count')
        ).join(OrmSymptom, OrmSymptom.patient_id == OrmPatient.patient_id).
            group_by(OrmPatient.patient_id)
    ).all()



    dy_query = (
        db.session.query(
            OrmSymptom.symptom_id,
            func.count(OrmDisease.disease_id).label('disease_count')
        ).join(OrmDisease, OrmDisease.symptom_id == OrmSymptom.symptom_id).
            group_by(OrmSymptom.symptom_id)
    ).all()



    patient_id, symptom_count = zip(*my_query)

    bar = go.Bar(
        x=patient_id,
        y=symptom_count
    )

    description, disease_count = zip(*dy_query)
    pie = go.Pie(
        labels=description,
        values=disease_count
    )

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphs_json)



@app.route('/plot', methods=['GET', 'POST'])
def medicine_plot():

    med_query = (
        db.session.query(
            OrmMedicine.medicine_name,
            OrmMedicine.price
        )).all()


    medicine_name, price = zip(*med_query)
    bar_medicine = go.Bar(
        x=medicine_name,
        y=price
    )

    data = {
        "bar_medicine": [bar_medicine]
    }
    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plot.html', graphsJSON=graphs_json)




if __name__ == '__main__':
    app.debug = True
    app.run()




