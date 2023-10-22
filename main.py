from flask import Flask, render_template, request, redirect, url_for, make_response, session, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'NLqmCgARzzEwDjTFdZu4tEuJqrLAGeQQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///find-a-room.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)

class user(db.Model):
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

@app.route('/')
@app.route('/home')
def init():
    return render_template('index.html')
 

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/loginPage', methods=['GET'])
def loginPage():
    errorMessage = None
    successMessage = None
    if (request.args.get('error')):
        errorMessage = request.args.get('error')   

    if (request.args.get('success')):
        successMessage = request.args.get('success')       

    return render_template('login.html', errorMessage = errorMessage, successMessage = successMessage)

@app.route('/signup', methods=['GET'])
def signup():   
    return render_template('signup.html', errorMessage = request.args.get('error'))


@app.route('/addRoom', methods=['GET'])
def addRoom():
    errorMessage = None
    successMessage = None
    if (request.args.get('error')):
        errorMessage = request.args.get('error')   

    if (request.args.get('success')):
        successMessage = request.args.get('success')       
    return render_template('addRoom.html',errorMessage = errorMessage, successMessage = successMessage)

@app.route('/roomInformation', methods=['POST'])
def roomInformation():
    roomDetail = None
    try:
        roomId = request.form['post_id'].strip()
        roomDetail =  db.session.query(roomdetails).filter(roomdetails.id == roomId).first()
        userInformation = db.session.query(user).filter(user.id == roomDetail.user_id).first()
    except Exception as e:
        print("Error occurred:", e)

    return render_template('roomDetails.html', roomDetail = roomDetail, user = userInformation)

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == "POST":

        user_exists = None

        try:
            username = request.form['username'].strip()
            password = request.form['password'].strip()
            user_exists =  db.session.query(user).filter(user.username == username and user.password == password).first()
        except Exception as e:
            user_exists = None
            print("Error occurred:", e)

        if (user_exists):
            session['loggedIn'] = True
            session['username'] = user_exists.username
            session['user_id'] = user_exists.id
            return redirect(url_for('init'))
        else:
            return redirect(url_for('loginPage', error= 'Username and/or Password invalid! Try Again!'))
    else:
        if "loggedIn" in session:
            return redirect(url_for('init'))

@app.route('/createUser', methods=['POST'])
def createUser():   

    if request.method == "POST":
        try:
            firstName = request.form['first_name'].strip()
            lastName = request.form['last_name'].strip()
            email = request.form['email'].strip()
            about = request.form['about'].strip()
            password = request.form['password'].strip()

            new_user = user(username=email, first_name=firstName, last_name=lastName, email=email, password=password, about=about)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('loginPage', success= 'User has been created!'))
        except Exception as e:
            print ("Error Occurred!:", e)
            return redirect(url_for('signup', error= 'Something went wrong. Try again!'))
    else:    
        return redirect(url_for('signup'))

@app.route('/createPost', methods=['POST'])
def createPost():   

    if request.method == "POST":
        try:
            postTitle = request.form['post_title'].strip()
            roomDescription = request.form['room_description'].strip()
            bedroom = request.form['bedroom'].strip()
            bathroom = request.form['bathroom'].strip()
            price = request.form['price'].strip()
            negotiable = request.form['neogitable'].strip()
            securityDep = request.form['securityDeposit'].strip()
            availability = request.form['availability'].strip()
            location = request.form['location'].strip()
            area = request.form['area_description'].strip()
            pets = request.form['pets'].strip()
            additional = request.form['additional'].strip()

            negotiable_val = False
            if(negotiable == "Yes"):
                negotiable_val = True

            pets_allowed_val = False
            if(pets == "Yes"):
                pets_allowed_val = True   

            date_obj = datetime.strptime(availability, '%Y-%m-%d').date()     

            new_post = roomdetails(post_title=postTitle, 
                                   room_description=roomDescription,
                                   rent_amount=price,
                                   location=location,
                                   security_deposit=securityDep,
                                   bed_number=bedroom,
                                   bath_number=bathroom,
                                   pets_allowed=pets_allowed_val,
                                   available_date=date_obj,
                                   area_description=area,
                                   additional_things=additional,
                                   negotiable=negotiable_val,
                                   user_id = session.get('user_id'))
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('addRoom', success= 'Your Post has been created!'))
        except Exception as e:
            print ("Error Occurred!:", e)
            return redirect(url_for('addRoom', error= 'Something went wrong. Try again!'))
    else:    
        return redirect(url_for('addRoom'))


@app.route('/logout', methods=['GET'] ) 
def logout():
    session.pop("loggedIn", None)
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect(url_for('loginPage'))


@app.route('/myListing', methods=['GET'] ) 
def myListing():
    errorMessage = None
    successMessage = None
    if (request.args.get('error')):
        errorMessage = request.args.get('error')   

    if (request.args.get('success')):
        successMessage = request.args.get('success')     
    user_id = session.get('user_id')
    try:
        roomList =  db.session.query(roomdetails).filter(roomdetails.user_id == user_id).all()
        return render_template('myListing.html',roomList = roomList, errorMessage = errorMessage, successMessage = successMessage)
    except Exception as e:
        print("Error occurred!", e)
        return redirect(url_for('init'))

@app.route('/searchRoom', methods=['POST'])
def searchRoom():

    try:
            keyword = request.form['keyword'].strip()
            budget = request.form['budget'].strip()
            location = request.form['location'].strip()
            bedroom = request.form['bedroom'].strip()
            bathroom = request.form['bathroom'].strip()

            roomList =  db.session.query(roomdetails).filter(roomdetails.post_title == keyword or roomdetails.rent_amount == budget or roomdetails.location == location or roomdetails.bed_number == bedroom or roomdetails.bath_number == bathroom).all()
        
            return render_template('roomListing.html', rooms = roomList) 
    
    except Exception as e:
            print ("Error Occurred!:", e)
            return redirect(url_for('addRoom', error= 'Something went wrong. Try again!'))
    
@app.route('/delete', methods=['POST'])
def deletePost():

    try:
            postId = request.form['post_id'].strip()
            room =  db.session.query(roomdetails).get_or_404(postId)
            db.session.delete(room)
            db.session.commit()
            
            return redirect(url_for('myListing', success="Deleted successfully!"))
    
    except Exception as e:
            print ("Error Occurred!:", e)
            return redirect(url_for('addRoom', error= 'Something went wrong. Try again!'))
    

@app.route('/editPost', methods=['POST'])
def editPost():

    try:
            postId = request.form['post_id'].strip()
            roomDetail =  db.session.query(roomdetails).filter(roomdetails.id == postId).first()            
            return render_template('editRoom.html',roomDetail = roomDetail)
    except Exception as e:
            print ("Error Occurred!:", e)
            return redirect(url_for('editRoom', error= 'Something went wrong. Try again!'))
    
@app.route('/updateRoom', methods=['POST'])
def updateRoom():

    try:
            postId = request.form['post_id'].strip()

            room = db.session.query(roomdetails).get_or_404(postId)  

            postTitle = request.form['post_title'].strip()
            roomDescription = request.form['room_description'].strip()
            bedroom = request.form['bedroom'].strip()
            bathroom = request.form['bathroom'].strip()
            price = request.form['price'].strip()
            negotiable = request.form['neogitable'].strip()
            securityDep = request.form['securityDeposit'].strip()
            availability = request.form['availability'].strip()
            location = request.form['location'].strip()
            area = request.form['area_description'].strip()
            pets = request.form['pets'].strip()
            additional = request.form['additional'].strip()

            negotiable_val = False
            if(negotiable == "Yes"):
                negotiable_val = True

            pets_allowed_val = False
            if(pets == "Yes"):
                pets_allowed_val = True   

            date_obj = datetime.strptime(availability, '%Y-%m-%d').date()     

            room.post_title=postTitle
            room.room_description=roomDescription
            room.rent_amount=price
            room.location=location
            room.security_deposit=securityDep
            room.bed_number=bedroom
            room.bath_number=bathroom
            room.pets_allowed=pets_allowed_val
            room.available_date=date_obj
            room.area_description=area
            room.additional_things=additional
            room.negotiable=negotiable_val
           
            db.session.commit()
            return redirect(url_for('myListing', success = 'Edited successfully!'))
    
    except Exception as e:
            print ("Error Occurred!:", e)
            return redirect(url_for('editPost', error= 'Something went wrong. Try again!'))    
        
if __name__ == '__main__':
        app.run(debug=True)