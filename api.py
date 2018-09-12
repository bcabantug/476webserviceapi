import flask
from flask_basicauth import BasicAuth
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

basic_auth = BasicAuth(app)

#dictionary function taken from programminghistorian for placement purposes
def dict_factory(cursor, row):
    d={}
    for idx, col in enumerate(cursor.description):
        d[col[0]]= row[idk]
    return d

#default for basic BasicAuth CHANGE
app.config['BASIC_AUTH_USERNAME'] = 'test'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'




@app.route('/', methods=['GET'])
def home():
    return '<h1>Initial Page</h1>'


@app.route('/forums', methods=['GET'])

def get_forum():
    # conn = sqlite3.connect('DiscussionForum.db')
    return '<h1>Forum return</h1>'
@app.route()

app.run()
