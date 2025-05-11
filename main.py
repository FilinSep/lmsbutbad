from flask import *
from utils import *
import checker
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import data.db_session as dses

from data.users import User
from data.login_form import LoginForm
from data.reg_form import RegisterForm
from data.code_form import CodeForm


login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'SECRET KEY 123123'


@login_manager.user_loader
def load_user(user_id):
    db_sess = dses.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = dses.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, user=current_user)
    
    return render_template('login.html', title='Авторизация', form=form, user=current_user)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        return redirect('/')

    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = dses.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            return render_template('reg.html',
                               message="Этот Email уже занят",
                               form=form, user=current_user)
            
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        return redirect('/')

    return render_template('reg.html', title='Авторизация', form=form, user=current_user)


@app.route('/')
def index():
    return render_template('home.html', user=current_user, tasks=get_list_of_tasks())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/rating')
def rating():
    db_sess = dses.create_session()

    if not current_user.is_authenticated:
        return redirect('/auth')
    
    return render_template('rating.html', rating=reversed(list(db_sess.query(User).order_by(User.rating).limit(10))), user=current_user, enumerate=enumerate)


@app.route('/task/<uid>', methods=['GET', 'POST'])
def task(uid):
    if not task_exists(uid):
        return redirect('/')
    
    content = request.cookies.get(f'{uid}_tf')

    form = CodeForm()
    if current_user.is_authenticated:
        resp = make_response(render_template('task.html', task=read_task(uid), user=current_user, status=get_task_status(current_user.id, uid), form=form))

        if form.validate_on_submit():
            resp.set_cookie(f'{uid}_tf', form.code.data)

            st = dses.create_session().query(TaskStatus).filter(TaskStatus.task == uid, TaskStatus.user_id == current_user.id).first()

            if not st or st.status == 'ERROR':
                checker.run(current_user.id, uid, form.code.data)

        else:
            form.code.data = content if content else '# Пишите код тут\n\nprint("Hello, World!")'

        return resp
    
    return redirect('/auth')


@app.route('/auth')
def auth():
    return render_template('noauth.html', user=current_user)


if __name__ == "__main__":
    dses.global_init('db/datab.db')
    app.run()