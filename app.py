from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/swe'

db = SQLAlchemy(app)
manager = Manager(app)

class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String)
	author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
	price = db.Column(db.Float)
	type = db.Column(db.String)

	def __repr__(self):
		return '<Book %r>' % self.title

class Author(db.Model):
	__tablename__ = 'authors'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	birth_date = db.Column(db.Date)
	bio = db.Column(db.Text)
	books = db.relationship('Book', backref='author')

	def __repr__(self):
		return '<Author %r>' % self.name

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/books/')
def books():
	b = Book.query.all()
	return render_template('books.html', books=b)

@app.route('/authors')
def authors():
	a = Author.query.all()
	return render_template('authors.html', authors=a)

def shell_context():
	context = {
		'app': app,
		'db': db,
		'Book': Book,
		'Author': Author
	}
	return context

manager.add_command('shell', Shell(make_context=shell_context))

if __name__ == "__main__":
        manager.run()
