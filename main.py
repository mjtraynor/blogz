from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:qwerty@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'fej4s8iku332sv56'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    blog = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, blog, owner):
        self.title = title
        self.blog = blog
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

def no_entry(text):
    if not text:
        return " is required."

def length_check(text):
    if len(text) < 3:
        return " must have at least 3 characters."

def password2_check(password, password2):
    if password != password2:
        return "Password 2 must match password."

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'view_blogs', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    show_all = User.query.all()
    return render_template('index.html', users=show_all)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user:
            if user.password == password:
                session['username'] = username
                flash("Logged in")
                return redirect('/new_blog')
            else:
                flash("Incorrect password entered")
                return redirect('/login')         
        else:
            flash('User does not exist')
            return redirect('/login')

## Need to add something here about what happend if they want to create an account, and get redirected to /signup

    return render_template('login.html')    

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            if no_entry(username):
                flash("Username" + no_entry(username))
                return redirect('/signup')
            elif length_check(username):
                flash("Username" + length_check(username))
                return redirect('/signup')
            if no_entry(password):
                flash("Password" + no_entry(password))
                return redirect('/signup')
            elif length_check(password):
                flash("Password" + length_check(password))
                return redirect('/signup')
            if password2_check(password, password2):
                flash(password2_check(password, password2))
                return redirect('/signup')   
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/new_blog')
        else:
            flash("Username already exists")
            return redirect('/signup')
    return render_template('signup.html')

@app.route('/new_blog', methods=['POST', 'GET'])
def new_post():
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        add_title = request.form['blog_title']
        add_blog = request.form['blog_post']

        add_all = Blog(add_title, add_blog, owner)

        if no_entry(add_title):
            flash("Title" + no_entry(add_title))
            return redirect('/new_blog')
        if no_entry(add_blog):
            flash("Blog post" + no_entry(add_blog))
            return redirect('/new_blog')
        db.session.add(add_all)
        db.session.commit()
        show_blog = "/all_blogs?id=" + str(add_all.id)
        return redirect(show_blog)
    else:
        return render_template('new_blog.html')

@app.route('/all_blogs')
def view_blogs():
    blog_id = request.args.get('id')
    user_id = request.args.get('user')

    if blog_id:
        view_blog=Blog.query.get(blog_id)
        return render_template('view_blog.html', blog=view_blog)
    if user_id:
        view_blog=Blog.query.get(blog_id)
        return render_template('singleUser.html', blogs=show_all)

    show_all = Blog.query.all()
    return render_template('all_blogs.html', blogs=show_all)

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/all_blogs')

if __name__ == '__main__':
    app.run()