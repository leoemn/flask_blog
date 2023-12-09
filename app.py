from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    posts = [
        {'title': 'First Post'},
        {'title': 'Second Post'},
        {'title': 'Third Post'},
    ]
    return render_template('index.html',message = 'this is message', posts = posts)

if __name__ == '__main__':
    app.run(debug=True)