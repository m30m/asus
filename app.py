import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

from actuator import Door, Lamp, Actuator
from sensor import Sensor, Motion, Noise, Proximity

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/proximity')
def proximity():
    return render_template('proximity.html')

@app.route('/noise')
def noise():
    return render_template('noise.html')

@app.route('/motion')
def motion():
    return render_template('motion.html')

@app.route('/lamp')
def lamp():
    return render_template('lamp.html')

@app.route('/door')
def door():
    return render_template('door_lock.html')


device_ids = {}
rules = []

@socketio.on('admin')
def handle_admin(message):
    print("%s connected" % (request.sid))
    app.admin_id = request.sid
    update_admin()


@socketio.on('act')
def handle_act(message):
    device_id = message['device_id']
    state = message['state']
    emit('act', {'state': state}, room=device_id)


@socketio.on('init')
def init_device(message):
    device_id = request.sid
    if message['type'] == 'door':
        device_ids[device_id] = Door(device_id, message['state'])
    if message['type'] == 'lamp':
        device_ids[device_id] = Lamp(device_id, message['state'])
    if message['type'] == 'motion':
        device_ids[device_id] = Motion(device_id)
        device_ids[device_id].recieve_state(message['state'])
    if message['type'] == 'noise':
        device_ids[device_id] = Noise(device_id)
        device_ids[device_id].recieve_state(message['state'])
    if message['type'] == 'proximity':
        device_ids[device_id] = Proximity(device_id)
        device_ids[device_id].recieve_state(message['state'])
    update_admin()


@socketio.on('update_state')
def update_state(message):
    print("%s connected" % (request.sid))
    print(message)
    device = device_ids[request.sid]
    if isinstance(device, Sensor):
        device.receive_state(message['state'])
    elif isinstance(device, Actuator):
        device.set_state(message['state'])
    print('received message: ' + str(message))
    update_admin()


@socketio.on('update_rules')
def update_rules(message):
    global rules
    rules = message
    print('updating rules')
    print(rules)


def update_admin():
    if app.admin_id is None:
        return
    devices = [{'id': x, 'state': device.get_state(), 'is_actuator': isinstance(device, Actuator)} for x, device in
               device_ids.items()]
    builder_rules = [
    ]
    for device in devices:
        builder_rules.append(
            {
                'type': 'radio',
                'label': 'Smart Door #%s' % device['id'][:4],
                'id': device['id'],
                'choices': [{'label': "Locked", 'value': False}, {'label': "Unlocked", 'value': True}]
            }
        )
    emit('update', {'devices': devices, 'builder_rules': builder_rules, 'rules': rules}, room=app.admin_id)


if __name__ == '__main__':
    app.admin_id = None
    socketio.run(app, debug=True, host='0.0.0.0')
