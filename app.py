from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    posts = [
        {'id': '1', 'title': 'First Post', 'content': 'Content of the first post'},
        {'id':'2', 'title': 'Second Post', 'content': 'Content of the second post'},
        {'id': '3', 'title': 'Third Post', 'content': 'Contetn of the third post'},
    ]

    return render_template('index.html', message = 'This is message', posts = posts)

@app.route('/post/<post_id>')
def post(post_id):
    posts = [
        {'id': '1', 'title': 'First Post', 'content': 'Content of the first post'},
        {'id':'2', 'title': 'Second Post', 'content': 'Content of the second post'},
        {'id': '3', 'title': 'Third Post', 'content': 'Contetn of the third post'},
    ]

    selected_post = next((post for  post in posts if post['id'] == post_id), None)

    if not selected_post:
        return render_template('404.html')
    
    return render_template('post.html', post = selected_post)

if __name__ == '__main__':
    app.run(debug = True)