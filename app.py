from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cruisehub.db'  # Adjust as needed
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cars = db.relationship('Car', backref='owner', lazy=True)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    reservations = db.relationship('Reservation', backref='car', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)


# Define Routes
@app.route('/')
def index():
    cars = Car.query.all()
    return render_template('index.html', cars=cars)

# ... other routes ...
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add User')

# Define the route for adding a user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()

    if form.validate_on_submit():
        # Create a new user based on the form data
        new_user = User(name=form.name.data)
        
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the index page or any other desired page
        return redirect(url_for('index'))

    return render_template('add_user.html', form=form)


# Run the Application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
