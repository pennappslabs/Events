from __future__ import absolute_import

from flask import render_template, session, g
from bson.objectid import ObjectId

from app import app
from app.views.helpers import jsonify


@app.route('/all', methods=['GET'])
@app.route('/login', methods=['GET'])
@app.route('/create', methods=['GET'])
@app.route('/user/<user>', methods=['GET'])
@app.route('/')
def index(user=None):
    user_id = session.get('user', None)
    if user_id:
        user = g.db.users.find_one({'_id': ObjectId(user_id)})
    else:
        user = {}
    if user:
        del user['hashed_password']
        user['logged_in'] = True
    return render_template('index.html', user=jsonify(user))
