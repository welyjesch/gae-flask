"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, request, render_template, json, jsonify
from google.appengine.ext import db
import datetime, logging

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


class Entry(db.Model):
    title = db.StringProperty()
    content = db.StringProperty() 
    publish = db.DateTimeProperty()

@db.transactional()
def create_entry_txn(keyname, title, content):
    que = db.Query(Entry)

    hasPost = db.GqlQuery("""SELECT * FROM Entry WHERE title = :1 """, title)

    if hasPost == None:
        return False
    else:
        newPost = Entry(
            title = request.form.get('title'),
            content = request.form.get('title'),
            publish = datetime.datetime.now()
        )

        db.put(newPost)
        return True

def get_entries_txn(page):
    que = db.Query(Entry)
    pages = 10 * int(page)
    entries = que.fetch(10, pages)
    logging.info(entries)
    return entries

@app.route('/')
def index():
    page = render_template('_base.htm')
    return page

@app.route('/post', methods=['GET', 'POST'])
def postEntry():
    error = None
    message = None
    if request.method == 'POST':
        if request.form['title'] == '':
            error = 'Invalid title'
            if request.form['content'] == '':
                error = 'Invalid content'
            if error == None:
                entryKeyname = request.form.get('keyname')
                entryTitle = request.form.get('title')
                entryContent = request.form.get('content')

                try:
                    canCreate = create_entry_txn(entryKeyname, entryTitle, entryContent)
                    if canCreate:
                        message = 'Successfully Posted'
                    else:
                        error = 'Post Title Exists'
                except db.TransactionFailedError, e:
                    logging.info(e)
        else:
            logging.info(error)

    pageVars = {
        'message': message,
        'error': error
    }

    logging.info(pageVars)

    page = render_template('post-new.htm', pvars = pageVars)
    return page

@app.route('/getEntries', methods=['GET'])
def getEntries():
    error = None
    message = None
    logging.info(request.args['page'])
    if request.method == 'GET':
        if request.args['page'] != None and request.args['page'] != '':
            page = request.args['page']
            try:
                entries = get_entries_txn(page)
                if entries:
                    return json.dump(entries)
                
            except db.TransactionFailedError, e:
                logging.info(e)
        else:
            logging.info(error)

    return jsonify(status='fail')

@app.route('/entry/new')
def saveEntry():
    postinfo = self.request
    self.response.out.write(postinfo)

    memo = Memo(parent=memo_key)

    if users.get_current_user():
      memo.author = users.get_current_user()
    memo.title = self.request.get('title')
    memo.content = self.request.get('content')
    memo.put()

@app.route('/entries')
def show_entries():
    x = 0
    testEntry = {
        'id' : 12345, 
        'title': 'test entry', 
        'featureImg': '/img/Jumbotron.jpg', 
        'description': 'this is a test description'
        }
    entries = []
    while x < 10:
        entries.append(testEntry)
        x += 1
    return jsonify(
            data=entries
        )

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
