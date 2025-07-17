from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db, login_manager


from .logger import app_logger, error_logger, warn_logger
from .logger import app_logger, error_logger, warn_logger
from .monitor import get_system_stats
from .models import FailedLoginLog, LoginLog
from sqlalchemy import text
from datetime import datetime, timedelta


main = Blueprint('main', __name__,template_folder='../templates')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')


from .models import LoginLog
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            login_user(user)
            flash("Giriş başarılı!")
           
            app_logger.info(f"Login SUCCESS: {user.username}")
            new_log = LoginLog(user_id=user.id)
            db.session.add(new_log)
            db.session.commit()
            return redirect(url_for('main.dashboard'))
        else:
            warn_logger.warning(f"Login FAILED: {form.username.data}")
            new_failed = FailedLoginLog(username_attempted=form.username.data)
            db.session.add(new_failed)
            db.session.commit()
            error_logger.error(f"ERROR olustu:{form.username.data}")
            
            
            flash("Kullanıcı adı veya parola yanlış.")
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        
        if existing_user:
            flash("⚠️ Bu kullanıcı adı zaten alınmış. Lütfen farklı bir ad deneyin.")
            warn_logger.warning(f"Kayitli kullanici: {form.username.data}")
            return render_template("register.html", form=form)
        
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Kayıt başarılı! Giriş yapabilirsiniz.")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

from flask import render_template

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

from sqlalchemy import text
from flask import render_template
from flask_login import login_required, current_user

from sqlalchemy import text
from sqlalchemy import text
from flask_login import login_required

@main.route('/login-stats')
@login_required
def login_stats():
    # Kullanıcı bazlı login istatistikleri
    user_stats = db.session.execute(text("""
        SELECT 
            u.username AS username,
            YEAR(l.login_time) AS year,
            MONTH(l.login_time) AS month,
            COUNT(*) AS total_logins,
            MAX(l.login_time) AS last_login
        FROM login_log l
        JOIN user u ON l.user_id = u.id
        GROUP BY u.username, year, month
        ORDER BY year DESC, month DESC, total_logins DESC                              
    """)).fetchall()

    # Genel başarı/başarısızlık istatistikleri
    counts = db.session.execute(text("""
        SELECT
            (SELECT COUNT(*) FROM failed_login_log) AS failed_count,
            (SELECT COUNT(*) FROM login_log) AS success_count
    """)).fetchone()

    total = counts.failed_count + counts.success_count
    fail_rate = (counts.failed_count / total * 100) if total > 0 else 0

    return render_template(
        'login_stats.html',
        stats=user_stats,
        data=counts,
        fail_rate=fail_rate
    )



@main.route('/failed-login-stats')
def failed_login_stats():
    query = text("""
        SELECT username_attempted, COUNT(*) as total_failed, MAX(attempt_time) as last_attempt
        FROM failed_login_log
        GROUP BY username_attempted
        ORDER BY total_failed DESC
    """)
    results = db.session.execute(query).fetchall()
    return render_template('failed_login_stats.html', stats=results)





@main.route('/system-monitor')
def system_monitor():
    stats = get_system_stats()
    return render_template('system_monitor.html', stats=stats)



from datetime import datetime, timedelta
from sqlalchemy import text
from . import db
from .logger import warn_logger




def check_last_login():
    latest_login = db.session.execute(text("""
        SELECT MAX(login_time) as last_login FROM login_log
    """)).fetchone().last_login

    if latest_login and (datetime.utcnow() - latest_login) > timedelta(days=7):
        warn_logger.warning("7 gündür giriş yapılmadı!")

@main.route('/check_last_login')
def check_last_login_route():
    check_last_login()
    return "Check completed, log dosyasını kontrol et."








