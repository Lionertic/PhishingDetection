from . import home

@home.route('/')
def homepage():
    return "render_template('home/index.html" , 200


@home.route('/dashboard')
def dashboard():
       return "render_templat" , 200

