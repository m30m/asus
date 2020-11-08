import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

from actuator import Door, Lamp, Actuator
from rules import Rule
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


from state import device_ids
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
        device = Door(device_id, message['state'])
    elif message['type'] == 'lamp':
        device = Lamp(device_id, message['state'])
    elif message['type'] == 'motion':
        device = Motion(device_id)
        device.receive_state(message['state'])
    elif message['type'] == 'noise':
        device = Noise(device_id)
        device.receive_state(message['state'])
    elif message['type'] == 'proximity':
        device = Proximity(device_id)
        device.receive_state(message['state'])
    else:
        raise Exception("Unknown type")
    device_ids[device_id] = device
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
    for r in rules:
        print(r)
        rule = Rule(r)
        print(rule.root)
        print(rule.evaluate())
        rule.execute()
        r['status'] = rule.evaluate()
    print('updating rules')
    print(rules)
    update_admin() # to send the new rules status


def update_admin():
    if app.admin_id is None:
        return
    devices = [{'id': x,
                'state': device.get_state(),
                'is_actuator': isinstance(device, Actuator),
                'type': device.type
                } for x, device in device_ids.items()]
    builder_rules = [
    ]
    for device in device_ids.values():
        builder_rules.append(device.build_rule())
    emit('update', {'devices': devices, 'builder_rules': builder_rules, 'rules': rules}, room=app.admin_id)


if __name__ == '__main__':
    app.admin_id = None
    socketio.run(app, debug=True, host='0.0.0.0')
