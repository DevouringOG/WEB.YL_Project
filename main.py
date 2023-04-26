import datetime
import io
import os

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required

from data import db_session
from data.shoes import Shoe
from data.users import User
from forms.ShoeForm import ShoeForm
from forms.loginForm import LoginForm
from forms.registerForm import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.permanent_session_lifetime = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html", message="Incorrect login or password", form=form)
    return render_template("login.html", form=form, title="Login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/add_shoe", methods=["POST", "GET"])
def add_shoe():
    form = ShoeForm()
    if form.validate_on_submit():
        print(form.name.data, form.category.data, form.price.data)
        for i in form.images.data:
            path = f"static/img/{form.name.data}"
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + "/" + i.filename, "wb") as new_image:
                new_image.write(i.read())
        sess = db_session.create_session()
        shoe = Shoe(name=form.name.data,
                    category=form.category.data,
                    price=form.price.data)
        sess.add(shoe)
        sess.commit()
        return redirect("/")
    return render_template("shoe.html", form=form)


@app.route("/")
def index():
    sess = db_session.create_session()
    shoes_data = sess.query(Shoe).all()
    print(shoes_data)
    return render_template("shoes_list.html", shoes_data=shoes_data)


@app.route("/air")
def air():
    return render_template("base.html")


@app.route("/jordan")
def jordan():
    return render_template("base.html")


@app.route("/dunk")
def dunk():
    return render_template("base.html")


if __name__ == '__main__':
    db_session.global_init("db/users_data.db")
    app.run(debug=True)
