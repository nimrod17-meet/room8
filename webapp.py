from flask import Flask, url_for, flash, render_template, redirect, request, g, send_from_directory
from flask import session as login_session
from model import *
from werkzeug.utils import secure_filename
import locale, os
# from werkzeug.contrib.fixers import ProxyFix
# from flask_dance.contrib.github import make_github_blueprint, github

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.wsgi_app = ProxyFix(app.wsgi_app)
# blueprint = make_github_blueprint(
#     client_id="TODO",
#     client_secret="TODO",
# )
# app.register_blueprint(blueprint, url_prefix="/login")

engine = create_engine('sqlite:///room8.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
	items = session.query(Apartment).all()
	return render_template('home.html', items=items)

@app.route('/apartments')
def apartments():
	items = session.query(Apartment).all()
	return render_template('apartments.html', items=items)

def verify_password(email, password):
	customer = session.query(Customer).filter_by(email=email).first()
	if not customer or not customer.verify_password(password):
		return False
	g.customer = customer
	return True

# @app.route('/')
# def index():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     resp = github.get("/user")
#     assert resp.ok
#     return "You are @{login} on GitHub".format(login=resp.json()["login"])

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email is None or password is None:
			flash('Missing Arguments')
			return redirect(url_for('login'))
		if verify_password(email, password):
			customer = session.query(Customer).filter_by(email=email).one()
			flash('Login Successful, welcome, %s' % customer.name)
			login_session['name'] = customer.name
			login_session['email'] = customer.email
			login_session['id'] = customer.id
			return redirect(url_for('home'))
		else:
			# incorrect username/password
			flash('Incorrect username/password combination')
			return redirect(url_for('login'))

@app.route('/newCustomer', methods = ['GET','POST'])
def newCustomer():
    if  request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phoneNumber = request.form['phoneNumber']

        if name is None or email is None or password is None :
            flash("Your form is missing arguments")
            return redirect(url_for('newCustomer'))
        
        
        if session.query(Customer).filter_by(email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('newCustomer'))
        customer = Customer(name=name, email=email, phoneNumber=phoneNumber)
        customer.hash_password(password)
        session.add(customer)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('home'))
    
    else:
        return render_template('newCustomer.html')

@app.route('/addApartment', methods = ['GET','POST'])
def addApartment():
    if 'id' not in login_session:
        flash("You must be logged in for this page")
        return redirect(url_for('login'))
    if request.method == 'POST':
        address = request.form['address']
        description = request.form['description']
        price = request.form['price']
        tenantNum = request.form['tenantNum']
        #photo
        if address is None or description is None or price is None or tenantNum is None :

            flash("Your form is missing arguments")
            
            return redirect(url_for('addApartment'))
        apartment = Apartment(description=description, price=price, tenantNum=tenantNum, address = address)
        session.add(apartment)
        session.commit()
        if 'file' in request.files:
            file = request.files['file']
        #if file.filename == '':
         #   flash('No selected file')
          #  return redirect(url_for('addApartment'))
           
            if file and allowed_file(file.filename):
                filename = str(apartment.id) + "_" + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                apartment.set_photo(filename)
                session.add(apartment)
                session.commit()
            flash("Apartment added Successfully!")
            return redirect(url_for('home'))
    else:
        return render_template('addApartment.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/apartment/<int:apartment_id>")
def apartment(apartment_id):
	apartment = session.query(Apartment).filter_by(id=apartment_id).first()
	return render_template('apartment.html', apartment=apartment)

@app.route("/tenants/<int:tenants_id>")
def tenants(tenants_id):
	tenants = session.query(Tenant).filter_by(id=tenant_id).all()
	return render_template('tenants.html', tenants=tenants)

@app.route('/logout')
def logout():
	if 'id' not in login_session:
		flash("You must be logged in order to log out")
		return redirect(url_for('login'))
	del login_session['name']
	del login_session['email']
	del login_session['id']
	flash("Logged Out Successfully")
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)
