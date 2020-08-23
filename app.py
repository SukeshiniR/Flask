from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
logging.basicConfig(filename='error.log', level=logging.DEBUG)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    url = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    labels = db.Column(db.String(200), nullable=True)
    allow_comments = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = Articles(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = Articles.query.order_by(Articles.updated_at).all()
        return render_template('posts.htm', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = Articles.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Articles.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        post.url = request.form['url']
        post.location = request.form['location']
        post.labels = request.form['labels']
        post.allow_comments = int(request.form['allow_comments'])
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.htm', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        post_url = request.form['url']
        post_location = request.form['location']
        post_labels = request.form['labels']
        post_allow_comments = int(request.form['allow_comments'])
        new_post = Articles(title=post_title, content=post_content, author=post_author, url=post_url, location=post_location, labels=post_labels)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new.htm')

@app.route('/posts/culture')
def post_type_culture():
    return render_template('type/culture.htm')

@app.route('/posts/business')
def post_type_business():
    return render_template('type/business.htm')

@app.route('/posts/technology')
def post_type_technology():
    return render_template('type/technology.htm')

@app.route('/posts/nature')
def post_type_nature():
    return render_template('type/nature.htm')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('login/signup.htm')

@app.route('/search/result')
def search_result():
    q = request.args.get('q')
    return render_template('result.htm', query=q)

if __name__ == "__main__":
    app.run(debug=True)
