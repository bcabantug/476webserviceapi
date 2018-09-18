from flask import Flask, Response, request, jsonify, render_template, g
import click
from flask_basicauth import BasicAuth
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

# Global db variable
DATABASE = 'forum.db'

# @app.cli.command()

#definiton to establish the connection to the db once
def establish_dbconn(dbname, command):
    print ('db connected')


#sublass of BasicAuth
class NewAuth(BasicAuth):
    #override of check_credentials
    def check_credentials(username, password):
        #compare the username and password to the db
        #if found, return
        found = username == app.config['BASIC_AUTH_USERNAME'] and password == app.config['BASIC_AUTH_PASSWORD']
        if found:
            print('User authenticated')

# new_auth = NewAuth(app)


#dictionary function taken from programminghistorian for placement purposes
def dict_factory(cursor, row):
    d={}
    for idx, col in enumerate(cursor.description):
        d[col[0]]= row[idx]
    return d

#default for basic BasicAuth CHANGE
# app.config['BASIC_AUTH_USERNAME'] = 'test'
# app.config['BASIC_AUTH_PASSWORD'] = 'matrix'



#list home page DEFAULT
@app.route('/', methods=['GET'])
def home():
    return '<h1>Initial Page</h1>'

#list available discussion forums GET
@app.route('/forums', methods=['GET', 'POST'])
def forum():
    #creating a new discussion forum
    if request.method == 'POST':
        print('Posting forum')
    #request for all the present forums
    else:
        query = 'SELECT * FROM Forums;'
        '''
            [
                {
                    "id": 1,
                    "name": "redis",
                    "creator": "alice"
                },
                {
                    "id": 2,
                    "name": "mongodb",
                    "creator": "bob"
                }
            ]
        '''
        '''
            Commands for accessing sqlite3
            1. type sqlite3 into command
            2. sqlite> prompt will appear
            3. enter .read [File]
            4. .tables will show if file was read
        '''
        conn = sqlite3.connect('forum.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        all_forums = cur.execute(query).fetchall()

        return jsonify(all_forums)

#create a new discussion forum POST
# @app.route('/forums', methods=['POST'])
#     def post_forum():


#list threads in the specified forum GET
@app.route('/forums/<forum_id>', methods=['GET', 'POST'])
def thread(forum_id):
    #creating a new thread in a specified forum
    if request.method == 'POST':
        #posting a new thread
        print('Posting forum')
    else:
        query = 'SELECT * from Threads WHERE'
        to_filter = []
        #return all the threads from the forum
        if forum_id:
            query += ' ForumId= '+str(forum_id)+';'
            to_filter.append(forum_id)
            conn = sqlite3.connect('forum.db')
            conn.row_factory = dict_factory
            cur = conn.cursor()
            all_threads = cur.execute(query).fetchall()

            return jsonify(all_threads)
        if not forum_id:
            return page_not_found(404)

#create a new thread in a specified forums POST

@app.route('/')


#list posts to the specified thread GET

@app.route('/forums/<forum_id>/<thread_id>', methods=['GET', 'POST'])
def post(forum_id, thread_id):
    if request.method == 'POST':
        print('Posting forum')
        #adding a new post to the specified thread
    else:
        #getting the posts for the specified thread
        print('Posting forum')
#add a new post to the specified thread POST

@app.route('/users', methods=['POST'])
def user():
    print('Posting forum')
#create a new user POST

#changes a user's password PUT
@app.route('/users/<username>', methods=['PUT'])
def change_pass(username):
    print('Posting forum')

# from http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
# Connects to and returns the db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#from http://flask.pocoo.org/docs/1.0/cli/
# CLI command for initlizing the db
@app.cli.command()
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('init.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print ('Database Initilaized')


if __name__ == "__main__":
    app.run()
