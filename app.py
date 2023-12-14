from flask import Flask, redirect, render_template, request, url_for
from  flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post',backref = 'author',lazy=True)

@app.route('/')
def home():

    posts = Post.query.all() 

    return render_template('index.html', message = 'This is message', posts = posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    
    selected_post = Post.query.get(post_id)

    if not selected_post:
        return render_template('404.html')
    
    return render_template('post.html', post = selected_post)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)