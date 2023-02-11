from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import pdb
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
# get not testing for ordering?

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    # GET /messages: returns an array of all messages as JSON
    # tests not testing for this??, ordered by created_at in ascending order.

    if request.method == 'GET':
        msgs = Message.query.all()
        msgs_serialized = [msg.to_dict() for msg in msgs]
        response = make_response(msgs_serialized, 200)
        
    elif request.method == 'POST':
        msg = Message(
            body= request.get_json()['body'], 
            username= request.get_json()['username']
        )
        db.session.add(msg)
        db.session.commit()
        response = make_response(msg.to_dict(), 201)

    return response

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    # PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
    msg = Message.query.filter_by(id=id).first()
    if request.method == 'PATCH':
        msg.body = request.get_json()['body']
        db.session.add(msg)
        db.session.commit()
        response = make_response(msg.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(msg)
        db.session.commit()
        response = make_response({'message': 'successfully deleted'}, 200)

    return response

if __name__ == '__main__':
    app.run(port=5555)
