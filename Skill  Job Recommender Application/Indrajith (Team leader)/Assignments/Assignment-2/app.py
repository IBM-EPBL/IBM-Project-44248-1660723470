from flask import Flask,render_template
app=Flask(__name__)
@app.route("/home")
def homepage():
 return render_template('home.html')
@app.route("/about")
def  aboutpage():
 return render_template('about.html')
@app.route("/sign in")
def signinpage():
  return render_template('sign in.html')
@app.route("/sign up")
def signuppage():
 return render_template('sign up.html')
if __name__=="__main__":
 app.run(debug=True)