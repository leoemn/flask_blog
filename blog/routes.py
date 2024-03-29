import os
import secrets
from PIL import Image
from flask import redirect, render_template, url_for, request, flash
from blog import app, db, bcrypt,login_manager
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from blog.models import User,Post
from flask_login import current_user,login_user, logout_user,login_required

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
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post()
        new_post.title = form.title.data
        new_post.content = form.content.data
        new_post.user_id = current_user

        db.session.add(new_post)
        db.session.commit()
        flash('Post has been created', 'success')
        return redirect(url_for('home'))
    
    return render_template('create_post.html', title = 'New Post', form = form)

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
        return redirect(url_for('home'))

    return render_template('register.html', title = 'SignUp', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_name = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/profile_pics', image_name)
    
    image_size = (125, 125)
    i = Image.open(form_image)
    i.thumbnail(image_size)
    i.save(image_path)

    return image_name

@app.route('/account',methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.image.data:
            new_image = save_image(form.image.data)
            current_user.image_file = new_image
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been Updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
         
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)
