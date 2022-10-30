from flask import Flask,render_template
app = Flask(__name__)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
 return render_template('index.html')


@app.route('/signup.html')
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


if __name__ == '__main__':
    app.run(port=5000,debug=True)


