from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

app = Flask(__name__)



@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
 return render_template('index.html')


@app.route('/signup.html', methods = ['POST', 'GET'])
def signup():
    return render_template('signup.html')

@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/index.html')
def home():
    return render_template('index.html')


@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/record',methods = ['POST','GET'])  # type: ignore
def record():
   if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

         
        with sql.connect("student_database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (name,email,phone,password) VALUES (?,?,?,?)",(name,email,phone,password) )
            con.commit()
            msg = "Record successfully added!"


        con = sql.connect("student_database.db")
        con.row_factory = sql.Row 
        cur = con.cursor()
        cur.execute("select * from users")
        users = cur.fetchall();
        return render_template("list.html",users = users)



if __name__ == '__main__':
    app.run(debug=True)


