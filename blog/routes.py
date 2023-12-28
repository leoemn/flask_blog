from flask import redirect, render_template, url_for, request, flash
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm
from blog.models import User,Post
from flask_login import current_user,login_user, logout_user

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
    
    return render_template('post.html', post =  selected_post)

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
    if current_user.is_authenticated:
        return redirect(url_for('login'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('You have loged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed, check your email and password', 'danger')

    return render_template('login.html', title = 'Login', form = form)


# Route for handling user sign up
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User()
        new_user.username = form.username.data
        new_user.email = form.email.data
        new_user.password = hashed_pw
        db.session.add(new_user)
        db.session.commit()
        flash(f"Account was created!",'success')
        return redirect('home')

    return render_template('register.html', title = 'SignUp', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
