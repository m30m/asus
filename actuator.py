from flask_socketio import emit

from device import Device


class Actuator(Device):

    def __init__(self, actuator_id, value_type, value_range, initial_state):
        super().__init__(actuator_id, value_type, value_range)
        self.state = None
        self.set_state(initial_state)

    def get_state(self):
        return self.state

    def set_state(self, state):
        if self.state_type == "continuous":
            try:
                float(state)
            except Exception:
                return
            if (self.range is not None) and (state > self.range[1] or state < self.range[0]):
                return

        elif self.state_type == "discrete" and (state not in self.range):
            return

        self.state = state
        emit('act', {'state': state}, room=self.device_id)


class Lamp(Actuator):
    type = 'lamp'

    def __init__(self, actuator_id, initial_state):
        super().__init__(actuator_id, "continuous", (0, 1), initial_state)

    def build_rule(self):
        return {
            'type': 'numeric',
            'label': 'Lamp #%s' % self.device_id[:4],
            'id': self.device_id,
        }


class Door(Actuator):
    type = 'door'

    def __init__(self, actuator_id, initial_state):
        super().__init__(actuator_id, "discrete", [False, True], initial_state)

    def build_rule(self):
        return {
            'type': 'radio',
            'label': 'Smart Door #%s' % self.device_id[:4],
            'id': self.device_id,
            'choices': [{'label': "Is Locked", 'value': False}, {'label': "Is Unlocked", 'value': True}]
        }
