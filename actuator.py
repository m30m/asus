from flask_socketio import emit

from device import Device
from state import device_names


class Actuator(Device):

    def __init__(self, actuator_id, value_type, value_range, initial_state):
        super().__init__(actuator_id, value_type, value_range)
        self.state = None
        self.set_state(initial_state)

    def get_state(self):
        return self.state

    def set_state(self, state):
        if self.state_type == "continuous":
            state = float(state)
            if (self.range is not None) and (state > self.range[1] or state < self.range[0]):
                raise Exception("Invalid value", state)

        elif self.state_type == "discrete" and (state not in self.range):
            raise Exception("Invalid value", state)

        self.state = state
        emit('act', {'state': state}, room=self.device_id)


class Lamp(Actuator):
    type = 'lamp'

    def __init__(self, actuator_id, initial_state):
        super().__init__(actuator_id, "continuous", (0, 1), initial_state)

    def build_rule(self):
        return {
            'type': 'numeric',
            'label': 'Lamp: %s' % device_names[self.device_id],
            'id': self.device_id,
        }

    def get_state_label(self):
        return 'Brightness: %s' % self.get_state()


class Door(Actuator):
    type = 'door'

    def __init__(self, actuator_id, initial_state):
        super().__init__(actuator_id, "discrete", [False, True], initial_state)

    def build_rule(self):
        return {
            'type': 'radio',
            'label': 'Smart Door: %s' % device_names[self.device_id],
            'id': self.device_id,
            'choices': [{'label': "Is Locked", 'value': False}, {'label': "Is Unlocked", 'value': True}]
        }

    def get_state_label(self):
        if self.get_state():
            return 'Unlocked'
        else:
            return 'Locked'