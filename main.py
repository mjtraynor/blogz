from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SconQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:qwerty@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.text)
    blog = db.Column(db.text)

    def __init__(self, title, blog):
        self.title = title
        self.blog = blog

def blank(text):

    if text:
        return False
    else:
        return True

@app.route(/all_blogs)
def view_blogs():

    show_all = Blog.query.all()
    render_template('all_blogs.html', blogs=show_all)

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():

    title_error = ""
    blog_error = ""

    if request.method == 'POST':
        add_title = request.form['new_title']
        add_blog = request.form['new_blog']
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
            return redirect(/all_blogs)
        
    else:
        render_template(/new_post)

if __name__ == '__main__':
    app.run()