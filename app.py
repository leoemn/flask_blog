from flask import Flask, redirect, render_template, url_for, request, flash
from  flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'AbCDefGHIjklmnOPqRsTuVwxyZ'

db = SQLAlchemy(app)


# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key =  True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

# Route for the home page
@app.route('/')
def home():

    posts = Post.query.all() 

    return render_template('index.html', posts = posts)

# Route for the about page
@app.route('/about')
def about():

    return render_template('about.html', title = 'About Page')

# Route for displaying an individual post
@app.route('/post/<int:post_id>')
def post(post_id):
    
    selected_post = Post.query.get(post_id)

    if not selected_post:
        return render_template('404.html')
    
    return render_template('post.html', post = selected_post)

# Route for creating a new post 
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post = Post()
        new_post.title = title
        new_post.content = content
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template('create_post.html')

# Route for handling user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()

    return render_template('login.html', title = 'Login', form = form)

# Route for handling user sign up
@app.route('/register', methods = ['GET', 'POST'])
def register():
    
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account was created!",'success')
        return redirect('/')

    return render_template('register.html', title = 'SignUp', form = form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)