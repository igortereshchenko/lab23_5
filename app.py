from flask import Flask, render_template, request, redirect
from forms.user_form import UserForm
from forms.feature_form import FeatureForm
from forms.remedy_form import RemedyForm
from forms.car_form import CarForm
import uuid
import json
import plotly
from sqlalchemy.sql import func
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vkntpqzmequvzy:d0cfa0ace686dbc41dd553bd05555159211f45db3571ab404cac94be19047fa8@ec2-174-129-254-231.compute-1.amazonaws.com:5432/dbm1daba6oq9rk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bdimrfldscvbhl:93372d5bf56ee8bdcb9e174c57a00a696f4984ab9fb852e2f4ad59e7a219144b@ec2-107-20-239-47.compute-1.amazonaws.com:5432/d9dgf2srlkpurp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class OrmUser(db.Model):
    __tablename__ = 'orm_user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    skin_condition = db.Column(db.Integer, nullable=False)
    feature = db.relationship('OrmFeature')
    car = db.relationship('Car')

class Car(db.Model):
    __tablename__ = 'orm_car'

    number = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('orm_user.user_id'))


class OrmFeature(db.Model):
    __tablename__ = 'orm_feature'

    feature_id = db.Column(db.Integer, primary_key=True)
    feature_name = db.Column(db.String(20), nullable=False)
    feature_size = db.Column(db.String(20), nullable=False)
    formtype = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('orm_user.user_id'))

    remedy = db.relationship('OrmRemedy')

class OrmRemedy(db.Model):
    __tablename__ = 'orm_remedy'
    remedy_id = db.Column(db.Integer, primary_key=True)
    remedy_name = db.Column(db.String(20), nullable=False)
    remedy_color = db.Column(db.String(20), nullable=False)
    remedy_brightness = db.Column(db.String(20), nullable=False)

    feature_id = db.Column(db.Integer, db.ForeignKey('orm_feature.feature_id'))


db.drop_all()

db.create_all()

John = OrmUser(
    user_id=1,
    user_name='John',
    user_age=19,
    skin_condition=7
)

Paul = OrmUser(
    user_id=2,
    user_name='Paul',
    user_age=20,
    skin_condition=3
)

George = OrmUser(
    user_id=3,
    user_name='George',
    user_age=30,
    skin_condition=8
)

Ringo = OrmUser(
    user_id=4,
    user_name='Ringo',
    user_age=25,
    skin_condition=5
)


Paul_nose = OrmFeature(
    feature_id=1,
    feature_name='nose',
    feature_size='small',
    formtype=6,
    user_id=2

)

Paul_lips = OrmFeature(
    feature_id=2,
    feature_name='lips',
    feature_size='big',
    formtype=6,
    user_id=2

)

John_nose = OrmFeature(
    feature_id=3,
    feature_name='nose',
    feature_size='big',
    formtype=6,
    user_id=1
)

George_eyes = OrmFeature(
    feature_id=4,
    feature_name='eyes',
    feature_size='medium',
    formtype=6,
    user_id=3

)

Pomade = OrmRemedy(
    remedy_id = 1,
    remedy_name = 'pomade',
    remedy_color = 'red',
    remedy_brightness = 'bright',
    feature_id=2
)

Shadows = OrmRemedy(
    remedy_id = 2,
    remedy_name = 'shadows',
    remedy_color = 'brown',
    remedy_brightness = 'light',
    feature_id=4
)

Conciller = OrmRemedy(
    remedy_id = 3,
    remedy_name = 'conciller',
    remedy_color = 'ivory',
    remedy_brightness = 'light',
    feature_id = 3
)

Poudre = OrmRemedy(
    remedy_id = 4,
    remedy_name = 'poudre',
    remedy_color = 'rose',
    remedy_brightness = 'medium',
    feature_id = 1
)

db.session.add_all([

    Paul,
    John,
    George,
    Ringo,
    John_nose,
    Paul_lips,
    Paul_nose,
    George_eyes,
    Pomade,
    Shadows,
    Conciller,
    Poudre
])

db.session.commit()


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/g', methods=['GET'])
def create_car():
    Alex = OrmUser(
        user_id=17,
        user_name='Alex',
        user_age=19,
        skin_condition=7
    )

    bmw = Car(
        number=123449,
        model='m5',
        color='black',
        price=100,
        user_id=17
    )
    audi = Car(
        number=123549,
        model='q5',
        color='black',
        price=100,
        user_id=17
    )
    gm = Car(
        number=823549,
        model='qgff',
        color='blue',
        price=100,
        user_id=17
    )

    db.session.add(Alex)
    db.session.add_all([bmw, audi, gm])
    db.session.commit()
    return render_template('success.html')

@app.route('/s')
def cars():
    res = db.session.query(Car).all()

    return render_template('cars_table.html', cars=res)

@app.route('/create_car', methods=['POST', 'GET'])
def add_car():
    form = CarForm()

    if request.method == 'POST':
        new_car = Car(
            number=form.number.data,
            model=form.model.data,
            color=form.color.data,
            price=form.price.data,
            user_id= form.user_id.data
        )
        db.session.add(new_car)
        db.session.commit()
        return render_template('success.html')
    elif request.method == 'GET':
        return render_template('car_form.html', form=form)



@app.route('/users')
def users():
    res = db.session.query(OrmUser).all()

    return render_template('users_table.html', users=res)

@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form = UserForm()

    if request.method == 'POST':
        new_user = OrmUser(
            user_id=form.user_id.data,
            user_name=form.user_name.data,
            user_age=form.user_age.data,
            skin_condition=form.skin_condition.data
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template('success.html')
    elif request.method == 'GET':
        return render_template('user_form.html', form=form)


@app.route('/user_edit/<string:id>', methods=['GET', 'POST'])
def edit_user(id):
    form = UserForm()
    result = db.session.query(OrmUser).filter(OrmUser.user_id == id).one()

    if request.method == 'GET':

        form.user_id.data = result.user_id
        form.user_name.data = result.user_name
        form.user_age.data = result.user_age
        form.skin_condition.data = result.skin_condition

        return render_template('edit_user.html', form=form, form_name='edit user')
    elif request.method == 'POST':

        result.user_name = form.user_name.data
        result.user_age = form.user_age.data
        result.skin_condition = form.skin_condition.data

        db.session.commit()
        return redirect('/users')

@app.route('/delete_user/<string:id>', methods=['GET', 'POST'])
def delete_user(id):
    result = db.session.query(OrmUser).filter(OrmUser.user_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')

# feature
@app.route('/features')
def features():
    res = db.session.query(OrmFeature).all()

    return render_template('features_table.html', features=res)

@app.route('/new_feature', methods=['GET', 'POST'])
def new_feature():
    form = FeatureForm()

    if request.method == 'POST':
        new_feature = OrmFeature(
            feature_id=form.feature_id.data,
            feature_name=form.feature_name.data,
            feature_size=form.feature_size.data,
            formtype=form.formtype.data,
            user_id=form.user_id.data
        )
        db.session.add(new_feature)
        db.session.commit()
        return render_template('success.html')
    elif request.method == 'GET':
        return render_template('feature_form.html', form=form)

@app.route('/edit_feature/<string:id>', methods=['GET', 'POST'])
def edit_feature(id):
    form = FeatureForm()
    result = db.session.query(OrmFeature).filter(OrmFeature.feature_id == id).one()

    if request.method == 'GET':

        form.feature_id.data = result.feature_id
        form.feature_name.data = result.feature_name
        form.feature_size.data = result.feature_size
        form.formtype.data = result.formtype
        form.user_id.data = result.user_id

        return render_template('edit_feature.html', form=form, form_name='edit feature')
    elif request.method == 'POST':

        result.feature_name = form.feature_name.data
        result.feature_size = form.feature_size.data
        result.formtype = form.formtype.data
        result.user_id = form.user_id.data

        db.session.commit()
        return redirect('/features')


@app.route('/delete_feature/<string:id>', methods=['GET', 'POST'])
def delete_feature(id):
    result = db.session.query(OrmFeature).filter(OrmFeature.feature_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')


# remedy
@app.route('/remedys')
def remedys():
    res = db.session.query(OrmRemedy).all()

    return render_template('remedys_table.html', remedys=res)


@app.route('/new_remedy', methods=['GET', 'POST'])
def new_remedy():
    form = RemedyForm()

    if request.method == 'POST':
        new_remedy = OrmRemedy(
            remedy_id=form.remedy_id.data,
            remedy_name=form.remedy_name.data,
            remedy_color=form.remedy_color.data,
            remedy_brightness=form.remedy_brightness.data,
            feature_id=form.feature_id.data

        )
        db.session.add(new_remedy)
        db.session.commit()
        return render_template('success.html')
    elif request.method == 'GET':
        return render_template('remedy_form.html', form=form)


@app.route('/edit_remedy/<string:id>', methods=['GET', 'POST'])
def edit_remedy(id):
    form = RemedyForm()
    result = db.session.query(OrmRemedy).filter(OrmRemedy.remedy_id == id).one()

    if request.method == 'GET':

        form.remedy_id.data = result.remedy_id
        form.remedy_name.data = result.remedy_name
        form.remedy_color.data = result.remedy_color
        form.remedy_brightness.data = result.remedy_brightness
        form.feature_id.data = result.feature_id

        return render_template('edit_remedy.html', form=form, form_name='edit remedy')
    elif request.method == 'POST':

        result.remedy_name = form.remedy_name.data
        result.remedy_color = form.remedy_color.data
        result.remedy_brightness = form.remedy_brightness.data
        result.feature_id = form.feature_id.data

        db.session.commit()
        return redirect('/remedys')


@app.route('/delete_remedy/<string:id>', methods=['GET', 'POST'])
def delete_remedy(id):
    result = db.session.query(OrmRemedy).filter(OrmRemedy.remedy_id == id).one()

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
            OrmUser.user_id,
            func.count(OrmFeature.feature_id).label('feature_count')
        ).join(OrmFeature, OrmUser.user_id == OrmFeature.user_id).
            group_by(OrmUser.user_id)
    ).all()

    re_query = (
        db.session.query(
            OrmFeature.feature_id,
            func.count(OrmRemedy.remedy_id).label('remedy_count')
        ).join(OrmRemedy, OrmRemedy.feature_id == OrmFeature.feature_id).
            group_by(OrmFeature.feature_id)
    ).all()

    car_query = (
        db.session.query(
            Car.model,
            Car.price
        )).all()


    user_id, feature_count = zip(*my_query)

    bar = go.Bar(
        x=user_id,
        y=feature_count
    )

    feature_id, remedy_count = zip(*re_query)
    pie = go.Pie(
        labels=feature_id,
        values=remedy_count
    )

    model, price = zip(*car_query)
    pie_car = go.Pie(
        labels=model,
        values=price
    )

    data = {
        "bar": [bar],
        "pie": [pie],
        "pie_car":[pie_car]
    }
    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphs_json)


@app.route('/plot', methods=['GET', 'POST'])
def car_plot():

    car_query = (
        db.session.query(
            Car.model,
            Car.price
        )).all()


    model, price = zip(*car_query)
    pie_car = go.Pie(
        labels=model,
        values=price
    )

    data = {
        "pie_car": [pie_car]
    }
    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('car_plot.html', graphsJSON=graphs_json)


if __name__ == '__main__':
    app.debug = True
    app.run()