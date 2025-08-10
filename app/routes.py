from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db
from app.forms import LoginForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
import markdown

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Home', posts=posts, now=datetime.now())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/content/<slug>')
def content(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    # หากโพสต์มีรูปภาพหลัก
    if post.image_url is None:
        post.set_og_image('content_images/default_og.jpg')
    return render_template('content.html', post=post, now=datetime.now())

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    
    # ตรวจสอบว่าเจ้าของโพสต์เท่านั้นที่แก้ไขได้
    if post.author != current_user:
        abort(403)
    
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('content', slug=post.slug))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content
    
    return render_template('edit.html', title='Edit Post', form=form, post=post,now=datetime.now())

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    
    # ตรวจสอบว่าเจ้าของโพสต์เท่านั้นที่ลบได้
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
    
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            slug=form.slug.data,
            content=form.content.data,
            author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template('create.html', title='Create Post', form=form)