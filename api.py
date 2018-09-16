import flask
from flask_basicauth import BasicAuth
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#sublass of BasicAuth
class NewAuth(BasicAuth):
    #override of check_credentials
    def check_credentials(username, password):
        #compare the username and password to the db
        #if found

# basic_auth = BasicAuth(app)

#dictionary function taken from programminghistorian for placement purposes
def dict_factory(cursor, row):
    d={}
    for idx, col in enumerate(cursor.description):
        d[col[0]]= row[idk]
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


    else:

#create a new discussion forum POST
# @app.route('/forums', methods=['POST'])
#     def post_forum():


#list threads in the specified forum GET
@app.route('/forums/<forum_id>', methods=['GET', 'POST'])
def thread():
    #creating a new thread in a specified forum
    if request.method == 'POST':
        #posting a new thread
    else:
        #return all the threads from the forum


#create a new thread in a specified forums POST

@app.route('')


#list posts to the specified thread GET

@app.route('/forums/<forum_id>/<thread_id>', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        #adding a new post to the specified thread
    else:
        #getting the posts for the specified thread

#add a new post to the specified thread POST

@app.route('/users', methods=['POST'])
def user():

#create a new user POST

#changes a user's password PUT
@app.route('users/<username>', methods=['PUT'])
def change_pass():
    
#











app.run()
