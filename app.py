from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user, logout_user, login_required, current_user, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import InputRequired, Length


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'secretkey'

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 




@login_manager.user_loader
def load_user(user_id):
      return User.query.get(int(user_id))



# Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

# Form
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)],render_kw={"placeholder": "Kullanıcı Adı"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=30)],render_kw={"placeholder": "Parola"})


    submit= StringField("Register")

def validdate_username(self, username):
    user = User.query.filter_by(username=username).first()
    if user:
        raise ValueError("Bu kullanıcı adı alınmış.")
    

#Login Form
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)],render_kw={"placeholder": "Kullanıcı Adı"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=30)],render_kw={"placeholder": "Parola"})


    submit= StringField("Login")





# Routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')





@app.route('/login', methods=['GET', 'POST'])
def login():      
    form= LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            login_user(user)
            flash("Giriş başarılı!")
            return redirect(url_for('dashboard'))
        else:
            flash("Kullanıcı adı veya parola yanlış.")
    return render_template('login.html',form=form)  

@app.route('/logout', methods=['GET', 'POST'])

@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = LoginForm()
    if form.validate_on_submit():
    
        user=User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect(url_for('dashboard'))
        flash("Dashboard'a hoş geldiniz!")
    return render_template('dashboard.html')








@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
       
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("⚠️ Bu kullanıcı adı zaten alınmış. Lütfen farklı bir ad deneyin.")
            return render_template("register.html", form=form)
   
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Kayıt başarılı! Giriş yapabilirsiniz.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json  

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Eksik bilgi"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "⚠️ Bu kullanıcı adı zaten alınmış"}), 409

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "✅ Kayıt başarılı"}), 201



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
