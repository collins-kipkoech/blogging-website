from flask import Flask, render_template,url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = ''

posts = [
    {
        'author':'collins',
        'title':'football',
        'content':'i love football',
        'date_posted':'nov 2020'
    },
    {
        'author':'kipkoech',
        'title':'coding',
        'content':'i love coding',
        'date_posted':'nov 2020'
    }
]

@app.route('/')
def index():
    title = 'Blogging Website'
    return render_template('index.html',posts=posts,title=title)


if __name__ == '__main__':
    app.run(debug=True)