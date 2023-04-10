import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.logout', 'title': 'Выйти'},
        {'url': '.listpubs', 'title': 'Список статей'},
        {'url': '.listusers', 'title': 'Список пользователей'}]

db = None

@admin.before_request
def before_request():
    '''Установление связи с бд до выполнения запроса'''
    global db
    db = g.get('link_db')

@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


def login_admin():
    session['admin_logged'] = 1

def isLogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)         

@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    
    return render_template('admin/index.html', menu=menu, title='Админ панель')

@admin.route('/login', methods=['POST', 'GET'])
def login():
    if isLogged():
        return redirect(url_for('.index'))
    
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['psw'] == '12345':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('Неверное имя или пароль', 'error')

    return render_template('admin/login.html', title='Админка') 

@admin.route('/logout')
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))   

@admin.route('/list-pubs')
def listpubs():
    if not isLogged():
        return(url_for('.login'))

    list = []
    try:
        cur = db.cursor()
        cur.execute(f'SELECT title, text, url FROM posts')
        list = cur.fetchall()
    except sqlite3.Error as e:
        print('Ошибка получения статей из БД' + str(e))

    return render_template('admin/listpubs.html', title='Список статей', menu=menu, list=list)    

@admin.route('/listusers')
def listusers():
    if not isLogged():
        return(url_for('.login'))

    list = []
    try:
        cur = db.cursor()
        cur.execute(f'SELECT name, email FROM users')
        list = cur.fetchall()
    except sqlite3.Error as e:
        print('Ошибка получения статей из БД' + str(e))

    return render_template('admin/listusers.html', title='Список пользователей', menu=menu, list=list) 