# Flask Application Structure

## Project Folder:

Our project folder serves as the root directory for our Flask application.

## Application Package:

In Flask, applications are commonly organized as packages. A package is essentially a directory containing a special file named `__init__.py`. This file, even if empty, designates the directory as a package.

## Application Modules:

Within our package, we'll create various modules(forms.py, models.py, routes.py). Each module houses different parts of our application's functionality.

## Static Folder:

The `static` folder is designated for holding static assets such as CSS files, JavaScript files, images, etc. This folder is conventionally named `static`.

## Templates Folder:

The `templates` folder stores HTML templates used by our Flask application. Templates are where we define the structure of our web pages.

## Main Application File (e.g., run.py):

The main application file, such as `run.py`, is often the entry point of your application. It imports Flask app and run the application.
## Configuration File (e.g., config.py):

(!we need to create this)Configuration settings, such as database connections or secret keys, can be stored in a separate configuration file. This modular approach helps keep our configuration organized and separate from the main application logic.

## 1.HTML templates

First, we will create all the necessary HTML templates for our webapp, using jinja2. Flask uses the Jinja template library to render templates. In our application, we will use templates to render HTML which will display in the user's browser. In Flask, Jinja is configured to autoescape any data that is rendered in HTML templates.

## 2.routes.py
In our routes.py we will define all the routes and render our HTML templates. 
Use the @app.route decorator to define routes. Routes are URLs that your application can respond to:
```python
@app.route('/')
def home():
    return render_template('index.html', posts = posts)
```




