import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/lamp')
def lamp():
    return render_template('lamp.html')


device_ids = {}


@socketio.on('admin')
def handle_admin(message):
    print("%s connected" % (request.sid))
    app.admin_id = request.sid


@socketio.on('act')
def handle_act(message):
    device_id = message['device_id']
    status = message['status']
    emit('act', {'status': status}, room=device_id)


@socketio.on('sense')
def handle_message(message):
    print("%s connected" % (request.sid))
    print(message)
    device_ids[request.sid] = message['status']
    print('received message: ' + str(message))
    if app.admin_id:
        emit('update', device_ids, room=app.admin_id)


if __name__ == '__main__':
    app.admin_id = None
    socketio.run(app, debug=True)
