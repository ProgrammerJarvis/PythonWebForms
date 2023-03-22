from flask import Flask, render_template, request, redirect, url_for
import sqlite3

#creating the database if there isn't one
db = sqlite3.connect('database.db', check_same_thread=False)
db.execute("""CREATE TABLE IF NOT EXISTS todo_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    completed TEXT
    )""")
db.commit()

#makes so the program is able to run in the browser
app = Flask(__name__, static_folder="static") #To launch web app type into terminal: python -m flask run


#the homepage when you start the application
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

#login form and checking if credidentals match
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username =='admin' and password == '123':
            return redirect(url_for('work'))
            # return 'logged in'
        else:
            return 'Access denied, go back and try again :)'

    else:
        return render_template('login.html')


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = ''
    if request.method =='POST':
        name = request.form['name']

    return render_template('name.html', name=name)


#the to-do list webpage
@app.route('/work', methods=['GET', 'POST'])
def work():
    if request.method == 'POST':
        task_description = request.form['task_description']

        db.execute(f"""INSERT INTO todo_items 
        (item_name, completed) VALUES 
        ("{task_description}", "No")""")
        db.commit()
    
    data = db.execute('SELECT * FROM todo_items').fetchall()
    
    return render_template("work.html", data=data)


#delete function for each task
@app.route('/delete/<int:id>')
def delete(id):
    db.execute(f'DELETE FROM todo_items WHERE id={id}')
    db.commit()
    return redirect(url_for('work'))


#mark complete/mark incomplete function for each task
@app.route('/complete/<int:id>')
def complete(id):
    data = db.execute(f'SELECT * FROM todo_items WHERE id={id}').fetchone()
    if data[2] == 'Yes':
        status = 'No'
    else:
        status = 'Yes'

    db.execute(f'UPDATE todo_items SET completed="{status}" WHERE id={id}')
    db.commit()
    return redirect(url_for('work'))

