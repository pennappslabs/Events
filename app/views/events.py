from __future__ import absolute_import
from flask import g, request, session
from bson.objectid import ObjectId
from app.views.helpers import BSONAPI, register_api, signals, jsonify


#creates a signal to be called when an event is made
new_event_signal = signals.signal('new-event-signal')


class EventAPI(BSONAPI):
    @property
    def collection_name(self):
        return 'events'

    def post(self):
        entity = request.form.to_dict()
        self.collection.insert(entity)
        #signals that a new event was made
        new_event_signal.send(self, entity=entity, u_id=session['user'])
        return jsonify(entity)

register_api(EventAPI, 'event_api', 'events')


@new_event_signal.connect
def new_event_triggered(sender=None, **kwargs):
    """
    On the signalling of a new event, add the event to its creator's
    event list.
    """
    u_id = ObjectId(kwargs['u_id'])
    e_id = ObjectId(kwargs['entity']['_id'])
    #insert the event into the creator's event list
    g.db.users.update({'_id': u_id}, {'$push': {'events': e_id}}, upsert=True)
