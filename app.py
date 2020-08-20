from flask import Flask, url_for, escape, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/index')
def index():
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
    return render_template('index.html', name=name, movies=movies)


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
