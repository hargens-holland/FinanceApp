from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/myappdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes for serving HTML pages
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/wallet')
def wallet():
    return send_from_directory('public', 'wallet.html')

@app.route('/profile')
def profile():
    return send_from_directory('public', 'profile.html')

@app.route('/setting')
def setting():
    return send_from_directory('public', 'setting.html')

@app.route('/help-center')
def help_center():
    return send_from_directory('public', 'help-center.html')

@app.route('/transaction-detail')
def transaction_detail():
    return send_from_directory('public', 'transation-detail.html')

# API Routes
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'name': user.name,
            'email': user.email
        } for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        new_post = Post(
            user_id=data['user_id'],
            title=data['title'],
            content=data['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({
            'id': new_post.id,
            'title': new_post.title,
            'content': new_post.content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        posts = Post.query.join(User).all()
        return jsonify([{
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_name': post.author.name
        } for post in posts])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve static files
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)
