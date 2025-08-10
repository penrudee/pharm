from app import db, login 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import bleach
import markdown
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    content = db.Column(db.Text)  # Markdown content
    content_html = db.Column(db.Text)  # Rendered HTML
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                       'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                       'h1', 'h2', 'h3', 'h4', 'p', 'img']
        target.content_html = bleach.linkify(bleach.clean(
            markdown.markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Post.content, 'set', Post.on_changed_content)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))