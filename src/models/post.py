from app import db

class Post(db.Model):
    __tablename__ = 'posts' 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    image_filename = db.Column(db.String(255))
    # Specific to Business Posts
    address_line_1 = db.Column(db.String(255))
    address_line_2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    state = db.Column(db.String(100))
    website_link = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    hours_of_operation = db.Column(db.Text)
    # Specific to Personal Posts
    trip_purpose = db.Column(db.String(100))
    time_of_visit = db.Column(db.String(50))
    rating = db.Column(db.String(50))
    comments = db.relationship('Comment', backref='post', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    edited = db.Column(db.Boolean, default=False)