from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Post
from wtforms import SelectField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', 
                         choices=[
                             ('countryside', 'Countryside'),
                             ('durian-orchard', 'Durian Orchard'),
                             ('local-people', 'Local People'),
                             ('other', 'Other')
                         ],
                         validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    @staticmethod
    def get_category_choices():
        # Could fetch from database or config
        return [
            ('countryside', 'Countryside'),
            ('durian-orchard', 'Durian Orchard'),
            ('local-people', 'Local People'),
            ('other', 'Other')
        ]
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Store post_id if provided (for edit cases)
        self.category.choices = self.get_category_choices()
        if 'post_id' in kwargs:
            self.post_id = kwargs['post_id']
            
            
            
    def validate_slug(self, slug):
        # สำหรับการแก้ไขโพสต์ ให้ข้ามการตรวจสอบ slug ของตัวเอง
        if hasattr(self, 'post_id'):
            post = Post.query.get(self.post_id)
            if post.slug == slug.data:
                return
        
        # ตรวจสอบว่า slug ไม่ซ้ำ
        if Post.query.filter_by(slug=slug.data).first():
            raise ValidationError('This slug is already in use. Please choose a different one.')