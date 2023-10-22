from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///find-a-room.db'
db = SQLAlchemy(app)

with app.app_context():
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(255), unique=True, nullable=False)
        first_name = db.Column(db.String(255), nullable=False)
        last_name = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(255), nullable=False)
        password = db.Column(db.String(255), nullable=False)
        about = db.Column(db.Text, nullable=False)

        def __repr__(self):
            return f'<User {self.username}>'

    class roomdetails(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        post_title = db.Column(db.Text, nullable=False)
        room_description = db.Column(db.Text, nullable=False)
        rent_amount = db.Column(db.Float, nullable=False)
        location = db.Column(db.String(255), nullable=False)
        security_deposit = db.Column(db.Float, nullable=False)
        bed_number = db.Column(db.Integer, nullable=False)
        bath_number = db.Column(db.Integer, nullable=False)
        pets_allowed = db.Column(db.Boolean, nullable=False)
        available_date = db.Column(db.Date, nullable=False)
        area_description = db.Column(db.Text, nullable=False)
        additional_things = db.Column(db.Text, nullable=True)
        negotiable = db.Column(db.Boolean, nullable=False)
        user_id = db.Column(db.Integer, nullable=False)

        def __repr__(self):
            return f'<roomdetails {self.post_title}>'
    
    
    # create the table
    db.create_all()

    # insert a mock row
    user = User(username='johndoe', first_name='John', last_name='Doe',
                email='johndoe@example.com', password='password123',
                about='Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                    'Donec vel sodales arcu, a pulvinar magna. '
                    'Nulla facilisi. Sed vel consequat urna.')

    db.session.add(user)
    db.session.commit()
