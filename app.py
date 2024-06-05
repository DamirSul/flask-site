from flask import Flask, render_template
from config import Config
from models import db, Car
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

admin = Admin(app, name='MyAdmin', template_mode='bootstrap3')
admin.add_view(ModelView(Car, db.session))


@app.route('/check_db')
def check_db():
    cars = Car.query.all()
    return f'Found {len(cars)} cars in the database'

@app.route('/')
def home():
    cars = Car.query.all()
    return render_template('home.html', title="Home", cars=cars)

@app.route('/about')
def about():
    return render_template('about.html', title="About BMW")

@app.route('/rules')
def rules():
    return render_template('rules.html', title="Site Rules")

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_detail.html', car=car)

if __name__ == '__main__':
    app.run(debug=True)
