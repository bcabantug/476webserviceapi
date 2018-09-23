from flask import Flask, Response, request, jsonify, render_template, g, abort
from flask_basicauth import BasicAuth
import sqlite3
import json

app = Flask(__name__)
app.config["DEBUG"] = True

# Global db variable
DATABASE = 'forum.db'

# @app.cli.command()

# TODO: remove if not used
# definiton to establish the connection to the db once
def establish_dbconn(dbname, command):
    print ('db connected')

# From http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
# Connects to and returns the db used in init_db() and query_db()
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# From http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
# Closes the db at the end of each rquest for get_db()
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# From http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
# query: query as string; e.g. 'Select * from Users'
# args: query arguments, leave empty if no args; e.g. ['user', 'password']
# one: Set to true if only 1 row is required for query else keep false
# returns results of the query
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# dictionary function taken from programminghistorian for placement purposes
def dict_factory(cursor, row):
    d={}
    for idx, col in enumerate(cursor.description):
        d[col[0]]= row[idx]
    return d


#sublass of BasicAuth
class NewAuth(BasicAuth):
    #override of check_credentials
    # returns true if the username and password matches else returns false
    def check_credentials(self, username, password):
        user = query_db('SELECT Username, Password from Users where Username = ? and password = ?', [username, password], one=True)
        if user is not None:
            return True
        else:
            return False


#default for basic BasicAuth CHANGE
# app.config['BASIC_AUTH_USERNAME'] = 'test'
# app.config['BASIC_AUTH_PASSWORD'] = 'matrix'

#list available discussion forums GET
@app.route('/forums', methods=['GET', 'POST'])
def forum():
    #creating a new discussion forum
    if request.method == 'POST':
        # auth contains the username and Password
        auth = request.authorization
        # check_auth returns True or False depending on the credentials
        check_auth = NewAuth().check_credentials(auth.username, auth.password)
        # Abort 401 if not authorized
        if check_auth is False:
            abort(401)
        # #gets the json for the name request
        forum_submit = request.get_json()
        #parse the name from JSON
        forum_name = forum_submit.get('name')
        # If forumn name does't exist insert it into the db and return success
        # Else abort 409
        if query_db('SELECT ForumsName from Forums where ForumsName = ?', [request.get_json().get('name')], one=True) is None:
            print(auth.username, str(forum_name))
            query = 'INSERT into Forums (CreatorId, ForumsName) Values ((Select UserId from Users where Username = ?), ?);'
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute(query, (auth.username, str(forum_name)))
            conn.commit()
            return jsonify({'success': True}), 201, {'ContentType': 'application/json'}
        else:
            abort(409)
    #request for all the present forums
    elif request.method == 'GET':
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
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        all_forums = cur.execute(query).fetchall()

        return jsonify(all_forums)
    else:
        abort(405)

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
    elif request.method == 'GET':
        # Query to be used here
        '''SELECT Forums.ForumId as id, title, creator, timestamp
            from (select UserName as creator, timestamp, ThreadBelongsTo, title
        		    from (select AuthorId, PostsTimestamp as timestamp, ThreadBelongsTo, ThreadsTitle as title
        				from Posts
        				join Threads
        				on Posts.ThreadBelongsTo = Threads.ThreadId
        				group by Threads.ThreadId
        				having min(Posts.PostId)
        				order by Posts.PostId)
    		         join Users
    		         on AuthorId = Users.UserId)
            join Forums
            on id = ?
            order by id desc'''

        query = 'SELECT Forums.ForumId as id, title, creator, timestamp from (select UserName as creator, timestamp, ThreadBelongsTo, title from (select AuthorId, PostsTimestamp as timestamp, ThreadBelongsTo, ThreadsTitle as title from Posts join Threads on Posts.ThreadBelongsTo = Threads.ThreadId group by Threads.ThreadId having min(Posts.PostId) order by Posts.PostId) join Users on AuthorId = Users.UserId) join Forums on id = ? order by id desc'
        to_filter = []
        #return all the threads from the forum
        if forum_id:
            # TODO: Add timestamp to query and proper json identifiers
            # query += ' ForumId= '+str(forum_id)+';'
            # to_filter.append(forum_id)
            conn = sqlite3.connect(DATABASE)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            all_threads = cur.execute(query, [str(forum_id)]).fetchall()
            # If the the quey returns an empty result
            # e.g. http://127.0.0.1:5000/forums/100
            if all_threads == []:
                abort(404)
            else:
                return jsonify(all_threads)
        # What is an example of this case?
        if not forum_id:
            abort(404)
    else:
        abort(405)

#create a new thread in a specified forums POST

@app.route('/')
def index():
    # TODO: remove before submission
    # NewAuth example code
    basic_auth = NewAuth().check_credentials('cameron', 'test')
    if basic_auth is True:
        print ('Authenticated')
    elif basic_auth is False:
        print ('Not Authenticated')

    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#list posts to the specified thread GET
@app.route('/forums/<forum_id>/<thread_id>', methods=['GET', 'POST'])
def post(forum_id, thread_id):
    if request.method == 'POST':
        return('Posting forum')
        # TODO:adding a new post to the specified thread

    elif request.method == 'GET':
        # Get all posts from specified thread
        data = request.get_json()
        query = 'SELECT Username as author, Message as text, PostsTimestamp as timestamp from Posts join Users on AuthorId = UserId and ThreadBelongsTo = ?;'
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        # all_threads = cur.execute(query).fetchall()
        allPosts = cur.execute(query, [thread_id]).fetchall()
        if allPosts == []:
            return abort(404)
        else:
            return jsonify(allPosts)

@app.route('/users', methods=['POST'])
def user():
    # curl -X POST -H "Content-Type: application/json" -d '{"username": "tuvwxyz", "password": "123" }' http://localhost:5000/users
    data = request.get_json()
    username = data['username']
    password = data['password']
    query = 'SELECT Username FROM Users WHERE Username=?'
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
    # Was running into an issue regarding the execute statement and needed to include a ',' after data['username'] in order for the query
    # to be ran
    user = cur.execute(query, (data['username'],)).fetchall()

    if user == []:
        query = 'INSERT INTO Users (Username, Password) VALUES (?, ?);'
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        # Need to use parameterised queries so API can insert values for username and
        # password into the query at the places with a ?
        # sources:
        # https://stackoverflow.com/questions/32945910/python-3-sqlite3-incorrect-number-of-bindings
        # https://stackoverflow.com/questions/32240718/dict-object-has-no-attribute-id
        cur.execute(query, (data['username'], data['password']))
        conn.commit()
        return jsonify({'success': True}), 201, {'ContentType': 'application/json'}
    else:
        return abort(409)

#create a new user POST

#changes a user's password PUT
@app.route('/users/<username>', methods=['PUT'])
def change_pass(username):
    # auth contains the username and Password
    auth = request.authorization

    # check_auth returns True or False depending on the credentials
    check_auth = NewAuth().check_credentials(auth.username, auth.password)

    # password contain the value of the new password after getting it from data with the appropriate key
    data = request.get_json()
    password = data.get('password')

    # Query the db to determine if the username has an account
    query = "SELECT Username FROM Users WHERE Username=?"
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    # https://stackoverflow.com/questions/14861162/cursor-fetchall-returns-extra-characters-using-mysqldb-and-python
    # If using fetchall() there is a potential error because it returns a list of tuples rather than just one tuple
    user = cur.execute(query, [data.get('username')]).fetchone()

    if user == None:
        return abort(404)
    elif auth is False or check_auth is False:
        return abort(401)
    elif auth.username != username:
        return abort(409)
    else:
        query = "UPDATE Users SET Password=? WHERE Username=?"
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(query, (password, username))
        conn.commit()

        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}

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
