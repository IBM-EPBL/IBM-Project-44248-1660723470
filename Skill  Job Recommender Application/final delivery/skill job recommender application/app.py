# from turtle import st
from flask import Flask, render_template, request, redirect, url_for, flash ,session
from markupsafe import escape

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tvw97028;PWD=6toUskNV0LP9Pw6r", '', '')

print(conn)
print("Success")

app = Flask(__name__)
app.secret_key = "app.secret_key"

@app.route('/')
@app.route('/home.html')
def home():
    return render_template('home.html')


@app.route('/post.html')
def post():
    return render_template('post.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':

        work_name = request.form['work_name']
        com_name = request.form['com_name']
        skill = request.form['skill']
        address = request.form['address']
        email = request.form['email']
        lpa = request.form['lpa']

        sql = "SELECT * FROM seeker WHERE work_name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, work_name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('post.html', msg="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO seeker VALUES (?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, work_name)
            ibm_db.bind_param(prep_stmt, 2, com_name)
            ibm_db.bind_param(prep_stmt, 3, skill)
            ibm_db.bind_param(prep_stmt, 4, address)
            ibm_db.bind_param(prep_stmt, 5, email)
            ibm_db.bind_param(prep_stmt, 6, lpa)
            ibm_db.execute(prep_stmt)

        return render_template('index.html', msg="Your post has been updated Successfully")


@app.route('/jobs.html')
def jobs():
    seeker = []
    sql = "SELECT * FROM seeker"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        # print ("The Name is : ",  dictionary)
        seeker.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)

    if seeker:
        return render_template("jobs.html", seeker=seeker)

@app.route('/login.html', methods=['POST','GET'])
def login():
    if request.method == 'POST':
       # conn =connection()
        email = request.form["email"]
        password = request.form["password"]
        sql = "SELECT COUNT(*) FROM users WHERE EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        res = ibm_db.fetch_assoc(stmt)
        if res['1'] == 1:
            session['loggedin'] = True
            session['email'] = email
            return render_template('index.html')
        else:
            return render_template('login.html',msg="email/ Password is incorrect! ")
    else:
            return render_template('login.html')


@app.route('/signup.html', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        # conn = connection()
         try:
            sql = "INSERT INTO users VALUES('{}','{}','{}','{}')".format(request.form["name"],request.form["email"],request.form["phone"],request.form["password"])
            ibm_db.exec_immediate(conn,sql)
            return render_template('signup.html', msg="Successfully Signed up Login now to enter dashboard")
         except:
            return render_template('signup.html', msg="Account already exists! ")
    else:
            return render_template('signup.html')



@app.route('/index.html')
def index():
    return render_template('index.html')
    
@app.route('/about.html')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.config['SESSION_TYPE']= 'filesystem'
    app.run(host='0.0.0.0', port=5000, debug=True)
