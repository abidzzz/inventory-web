from flask import Flask
from flask import Flask, redirect, render_template, request, session , url_for
from jinja2 import TemplateNotFound

import mysql.connector as mycon
import os

app = Flask(__name__)

con = mycon.connect(host='localhost', user='root', passwd='bruh')

if con.is_connected:
    print(' * Connected to MySQL server')
    cur = con.cursor()
else:
    print('[!]  Not connected to MySQL')

db_query = "CREATE DATABASE IF NOT EXISTS inventory"
cur.execute(db_query)


con.database = 'inventory'

cur.execute("CREATE TABLE if not exists users (username varchar (20) PRIMARY KEY, password	varchar (20) NOT NULL, account_type varchar (10) NOT NULL);")
cur.execute("CREATE TABLE if not exists products (product_id varchar (20) PRIMARY KEY, product_name varchar (50) NOT NULL, description varchar (50) NOT NULL, price DECIMAL(10, 2) NOT NULL, quantity INTEGER NOT NULL);")
cur.execute("CREATE TABLE if not exists orders (receipt_no INTEGER PRIMARY KEY, invoice INTEGER NOT NULL, product_id varchar (20), quantity INTEGER NOT NULL, date varchar (20), time varchar (20));")

@app.context_processor
def set_global_html_variable_values():
    if session.get('acc_type') == 'ADMIN':
        admin_account = True
        username = session.get('username')
    else:
        username = False
        admin_account = False
    template_config = {'admin_account': admin_account, 'username':username}

    return template_config


@app.route('/')
@app.route('/dashboard')
def home():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    
    return redirect('/login')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':

            password = request.form['password']
            acc_type = request.form['acc_type']

            query = f'UPDATE users set password = "{password}", account_type = "{acc_type}" where username = "{username}" ;'
            cur.execute(query)
            con.commit()

        cur.execute(f"select * from users where username = '{username}'")
        users = cur.fetchall()

        return render_template('users.html', users = users)
    
    return redirect('/login')

@app.route('/users', methods=['GET', 'POST'])
def users():

    if 'username' in session:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            acc_type = request.form['acc_type']

            query = f'UPDATE users set password = "{password}", account_type = "{acc_type}" where username = "{username}" ;'
            cur.execute(query)
            con.commit()

        cur.execute("select * from users")
        users = cur.fetchall()

        return render_template('users.html', users = users)
    
    return redirect('/login')


@app.route('/orders')
def orders():
    if 'username' in session:
        cur.execute("select * from orders")
        orders = cur.fetchall()
        return render_template('orders.html', orders = orders)
    
    return redirect('/login')


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():

    if 'username' in session:
        if session['acc_type'] == "ADMIN" and request.method == 'POST':
            p_id = request.form['p_id']
            p_name = request.form['p_name']
            desc = request.form['desc']
            price = request.form['price']
            qty = request.form['quantity']
            query = f'''INSERT INTO products (product_id, product_name, description, price, quantity)
VALUES ('{p_id}', '{p_name}', '{desc}', {price},{qty});'''
            cur.execute(query)
            con.commit()
        cur.execute("select * from products")
        products = cur.fetchall()
        return render_template('inventory.html', products = products)
    
    return redirect('/login')

@app.route('/shop', methods=['GET', 'POST'])
def shop():

    if 'username' in session:
        if request.method == 'POST':
            order_id = request.form['p_id']
            p_name = request.form['p_name']
            desc = request.form['desc']
            price = request.form['price']
            qty = request.form['quantity']
            query = f'''INSERT INTO orders (order_id, invoice, product_id, quantity, date, time)
VALUES ('{order_id}', '{p_name}', '{desc}', {price},{qty});'''
            cur.execute(query)
            con.commit()
        cur.execute("select * from products")
        products = cur.fetchall()
        return render_template('inventory.html', products = products)
    
    return redirect('/login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cur.execute(query, (username, password))
        user = cur.fetchone()
        
        if user:
            session['username'] = username
            session['acc_type'] = user[2]
            return redirect('/')
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
        
    elif 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur.execute(f"select * from users where username='{username}'")
        f = cur.fetchall()
        if f:
            error = "Username already exist"
            return render_template('register.html', error=error)
        else:    

            if len(username)>20 or len(password)>20 :
                error = "Length of the Username and Password should be less than 20"
                return render_template('register.html', error=error)
                    
            cur.execute(f"insert into users values('{username}','{password}','USER')")
            con.commit()

            session['username'] = username
            return redirect('/')
    elif 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('acc_type', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)