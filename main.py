from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:qwerty@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

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

def blank(text):

    if text:
        return False
    else:
        return True

@app.route('/')
def redirect_main():
    return redirect('/all_blogs')

@app.route('/all_blogs')
def view_blogs():

    blog_id = request.args.get('id')

    if blog_id:
        view_blog=Blog.query.get(blog_id)
        return render_template('view_blog.html', blog=view_blog)
    else:
        show_all = Blog.query.all()
        return render_template('all_blogs.html', blogs=show_all)

@app.route('/new_blog', methods=['POST', 'GET'])
def new_post():

    title_error = ""
    blog_error = ""

    if request.method == 'POST':
        add_title = request.form['blog_title']
        add_blog = request.form['blog_post']
        add_all = Blog(add_title, add_blog)

        if blank(add_title):
            title_error = "You need to enter a title."
            if blank(add_blog):
                blog_error = "You need to make a blog entry."
            return render_template('new_blog.html', title_error=title_error, blog_error=blog_error)
        elif blank(add_blog):
            blog_error = "You need to make a blog entry."
            return render_template('new_blog.html', title_error=title_error, blog_error=blog_error)
        else:
            db.session.add(add_all)
            db.session.commit()
            show_blog = "/all_blogs?id=" + str(add_all.id)
            return redirect(show_blog)
    else:
        return render_template('new_blog.html')

if __name__ == '__main__':
    app.run()