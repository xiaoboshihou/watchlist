import os
import sys
import click
from flask import Flask, url_for, escape, render_template
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command()    # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')    # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'lxy'
    movies = [{'title': 'My Neighbor Totoro', 'year': '1988'},
              {'title': 'Dead Poets Society', 'year': '1989'},
              {'title': 'A Perfect World', 'year': '1993'},
              {'title': 'Leon', 'year': '1994'},
              {'title': 'Mahjong', 'year': '1996'},
              {'title': 'Swallowtail Butterfly', 'year': '1996'},
              {'title': 'King of Comedy', 'year': '1999'},
              {'title': 'Devils on the Doorstep', 'year': '1999'},
              {'title': 'WALL-E', 'year': '2008'},
              {'title': 'The Pork of Music', 'year': '2012'}]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/index')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/home')
def home():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)


@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='lxy'))
    print(url_for('user_page', name='herman'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'


if __name__ == '__main__':
    app.run()
