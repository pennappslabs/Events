import json

import bcrypt
from flask import session, request

from app import db
from helpers import BSONView, register_api, jsonify


PASSWORDS_DO_NOT_MATCH = 'Passwords do not match'
NO_PASSWORD_PROVIDED = 'No password provided'
UNAUTHORIZED_REQUEST = 'User is not logged in'


class UserAPI(BSONView):
    @property
    def collection_name(self):
        return 'users'

    def post(self):
        user = request.form.to_dict()
        # get password and hash it
        password = request.form.get('password', None)
        confirm = request.form.get('confirm', None)
        if password:
            if password == confirm:
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                user['hashed_password'] = hashed_password
                del user['password']
                del user['confirm']
                # insert returns an ObjectId
                user_id = str(db.users.insert(user))
                # abstract into pre-serialize user
                del user['hashed_password']
                user['logged_in'] = True
                session['user'] = user_id
                return jsonify(user)
            else:
                # password != confirm
                return json.dumps({'error': PASSWORDS_DO_NOT_MATCH})
        else:
            # no password was entered
            return json.dumps({'error': NO_PASSWORD_PROVIDED})


@app.route('/users/<f_id>/subscriptions', methods=['POST', 'DELETE'])
def subscriptions(f_id):
    u_id = session.get('user', None)
    if u_id:
        if request.method == 'POST':
            # TODO Merge the database requests
            # add f_id to u_id's following
            db.users.update({'_id': ObjectId(u_id)}, {'$push': {'following': f_id}}, {'upsert': True})
            # add u_id to f_id's followers
            db.users.update({'_id': ObjectId(f_id)}, {'$push': {'followers': u_id}}, {'upsert': True})
            # TODO Get f_id's events and add them to u_id's event queue
        else:
            # remove f_id from u_id's following
            # remove u_id from f_id's followers
            pass
    else:
        return json.dumps({'error': UNAUTHORIZED_REQUEST})


register_api(UserAPI, 'user_api', '/users/')
